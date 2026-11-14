'use strict';

// Execute the shipped browser scripts with a small DOM adapter. This checks
// their event-driven behavior; it does not replace browser or accessibility QA.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const logistics = path.resolve(__dirname, '../website-package/sites/logistics');

class Element {
  constructor(tag = 'div') {
    this.tagName = tag;
    this.children = [];
    this.listeners = new Map();
    this.textContent = '';
    this.value = '';
    this.checked = false;
  }

  append(...elements) { this.children.push(...elements); }
  appendChild(element) { this.append(element); return element; }
  replaceChildren(...elements) { this.children = [...elements]; }

  addEventListener(event, listener) {
    const listeners = this.listeners.get(event) || [];
    this.listeners.set(event, [...listeners, listener]);
  }

  fire(event) {
    const listeners = this.listeners.get(event);
    assert.ok(listeners?.length, `Expected a ${event} handler`);
    for (const listener of listeners) listener({ type: event, target: this });
  }

  querySelectorAll(selector) {
    assert.ok([
      'input[type="checkbox"]',
      'input[type="checkbox"]:checked',
    ].includes(selector), `Unsupported DOM adapter selector: ${selector}`);
    const descendants = (element) => element.children.flatMap(
      (child) => [child, ...descendants(child)],
    );
    return descendants(this).filter((element) => (
      element.tagName === 'input' && element.type === 'checkbox'
      && (!selector.endsWith(':checked') || element.checked)
    ));
  }
}

function runScript(relativePath, initialValues, ids) {
  const elements = Object.fromEntries(ids.map((id) => [id, new Element()]));
  for (const [id, value] of Object.entries(initialValues)) elements[id].value = value;
  const context = vm.createContext({
    document: {
      getElementById(id) {
        assert.ok(elements[id], `Unexpected DOM element: ${id}`);
        return elements[id];
      },
      createElement(tag) { return new Element(tag); },
    },
  });
  // Network, upload, and storage globals are intentionally absent. The supplied
  // synthetic examples must work with only document access.
  vm.runInContext(fs.readFileSync(path.join(logistics, relativePath), 'utf8'), context, {
    filename: relativePath,
    timeout: 1000,
  });
  return { elements, context };
}

function testShipmentChecklist() {
  const { elements } = runScript('demo/demo.js', { lane: 'fr-ma' }, [
    'lane', 'checks', 'score', 'notice', 'reset',
  ]);
  assert.equal(elements.score.textContent, '0 / 5 items marked present');

  for (const lane of ['fr-ma', 'fr-sn', 'ma-sn', 'ea']) {
    elements.lane.value = lane;
    elements.lane.fire('change');
    const boxes = elements.checks.querySelectorAll('input[type="checkbox"]');
    assert.equal(boxes.length, 5, `${lane} should have five sample items`);
    assert.equal(new Set(boxes.map((box) => box.id)).size, 5);
    assert.equal(elements.score.textContent, '0 / 5 items marked present');

    boxes[0].checked = true;
    boxes[0].fire('change');
    assert.equal(elements.score.textContent, '1 / 5 items marked present');
    assert.match(elements.notice.textContent, /^4 example item/);

    for (const box of boxes) box.checked = true;
    boxes[4].fire('change');
    assert.equal(elements.score.textContent, '5 / 5 items marked present');
    assert.match(elements.notice.textContent, /have NOT been verified/);

    boxes[0].checked = false;
    boxes[0].fire('change');
    assert.equal(elements.score.textContent, '4 / 5 items marked present');
    assert.match(elements.notice.textContent, /^1 example item/);

    elements.reset.fire('click');
    assert.equal(elements.score.textContent, '0 / 5 items marked present');
    assert.equal(elements.checks.querySelectorAll('input[type="checkbox"]:checked').length, 0);
    assert.match(elements.notice.textContent, /^5 example item/);
  }

  const oldBox = elements.checks.querySelectorAll('input[type="checkbox"]')[0];
  oldBox.checked = true;
  oldBox.fire('change');
  elements.lane.value = 'fr-ma';
  elements.lane.fire('change');
  assert.equal(elements.score.textContent, '0 / 5 items marked present');
  assert.equal(elements.checks.querySelectorAll('input[type="checkbox"]:checked').length, 0);
  assert.ok(!elements.checks.querySelectorAll('input[type="checkbox"]').includes(oldBox));
}

function testInvoiceReferences() {
  const { elements, context } = runScript('billing/demo/check.js', { scenario: 'match' }, [
    'scenario', 'fields', 'result', 'details',
  ]);
  assert.match(elements.result.textContent, /^No identifier mismatches found/);

  const expectedDetails = {
    match: /Human review is still necessary/,
    missing: /Invoice number must be recorded/,
    mismatch: /Invoice reference differs/,
    po: /Purchase-order references disagree/,
  };
  for (const [scenario, expectedDetail] of Object.entries(expectedDetails)) {
    elements.scenario.value = scenario;
    elements.scenario.fire('change');
    assert.equal(elements.details.children.length, 1);
    assert.match(elements.details.children[0].textContent, expectedDetail);
    assert.match(elements.result.textContent, scenario === 'match'
      ? /^No identifier mismatches found/
      : /^1 document-reference issue/);
    assert.match(elements.fields.textContent, /Invoice: VE-INV-001/);
    assert.match(elements.fields.textContent, scenario === 'missing'
      ? /Packing list: \(missing\)/
      : /Packing list: VE-INV-/);
  }

  // Missing PO references and simultaneous errors are not selectable demo
  // records, but are meaningful boundaries of the actual analysis function.
  const evaluate = (expression) => vm.runInContext(expression, context, { timeout: 1000 });
  assert.equal(evaluate("analyze({invoice:'VE-1',packing:'VE-1',orderInvoice:'',orderPacking:''}).length"), 1);
  assert.match(evaluate("analyze({invoice:'VE-1',packing:'VE-1',orderInvoice:'',orderPacking:''})[0]"), /purchase-order reference/);
  assert.equal(evaluate("analyze({invoice:'',packing:'',orderInvoice:'',orderPacking:''}).length"), 2);
  assert.equal(evaluate("analyze({invoice:'A',packing:'B',orderInvoice:'C',orderPacking:'D'}).length"), 2);

  elements.scenario.value = 'match';
  elements.scenario.fire('change');
  assert.match(elements.result.textContent, /^No identifier mismatches found/);
  assert.equal(elements.details.children.length, 1, 'Old failure details should be replaced');
  assert.match(elements.details.children[0].textContent, /Human review is still necessary/);
}

testShipmentChecklist();
testInvoiceReferences();
console.log('PASS: shipment checklist (4 lanes; initial, partial, complete, uncheck, reset, lane switch)');
console.log('PASS: invoice checker (4 scenarios; missing PO, combined errors, return to matching record)');
console.log('Scope: shipped JavaScript in Node VM with a minimal DOM adapter; browser layout, keyboard, screen-reader, and live subdomain tests remain required.');
