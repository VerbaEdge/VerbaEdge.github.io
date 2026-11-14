"use strict";
// All records fictional. No external network, uploads, storage, or personal data.
const scenarios=Object.freeze({
 match:{invoice:'VE-INV-001',packing:'VE-INV-001',orderInvoice:'PO-044',orderPacking:'PO-044'},
 missing:{invoice:'VE-INV-001',packing:'',orderInvoice:'PO-044',orderPacking:'PO-044'},
 mismatch:{invoice:'VE-INV-001',packing:'VE-INV-017',orderInvoice:'PO-044',orderPacking:'PO-044'},
 po:{invoice:'VE-INV-001',packing:'VE-INV-001',orderInvoice:'PO-044',orderPacking:'PO-140'}
});
const select=document.getElementById('scenario');
const fields=document.getElementById('fields');
const result=document.getElementById('result');
const details=document.getElementById('details');
function analyze(rec){
 const failures=[];
 if(!rec.invoice||!rec.packing) failures.push('Invoice number must be recorded in both invoice and packing-list metadata.');
 else if(rec.invoice!==rec.packing) failures.push('Invoice reference differs between the two document records.');
 if(!rec.orderInvoice||!rec.orderPacking) failures.push('Both document records require a purchase-order reference.');
 else if(rec.orderInvoice!==rec.orderPacking) failures.push('Purchase-order references disagree.');
 return failures;
}
function render(){
 const rec=scenarios[select.value], failures=analyze(rec);
 fields.textContent=`Invoice: ${rec.invoice || '(missing)'} | Packing list: ${rec.packing || '(missing)'} | Invoice PO: ${rec.orderInvoice || '(missing)'} | Packing-list PO: ${rec.orderPacking || '(missing)'}`;
 result.textContent=failures.length?`${failures.length} document-reference issue(s) flagged`:'No identifier mismatches found in this fictional record';
 details.replaceChildren();
 const notes=failures.length?failures:['No differences found in the two reference fields checked. Human review is still necessary.'];
 for (const note of notes){const li=document.createElement('li');li.textContent=note;details.appendChild(li);}
}
select.addEventListener('change',render);
render();
