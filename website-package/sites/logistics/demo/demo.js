"use strict";
// Example only. These lists are illustrative and are NOT jurisdiction-specific legal document requirements.
const lanes = Object.freeze({
  "fr-ma": ["Commercial invoice reference", "Packing list reference", "Transport document reference", "Named recipient or broker", "Shipment handoff contact"],
  "fr-sn": ["Commercial invoice reference", "Packing list reference", "Transport document reference", "Import documentation review owner", "Shipment milestone owner"],
  "ma-sn": ["Commercial invoice reference", "Packing list reference", "Transport document reference", "Origin information review", "Receiving team contact"],
  "ea": ["Commercial invoice reference", "Cargo manifest or transport reference", "Dispatch status owner", "Border handoff contact", "Delivery milestone owner"]
});
const lane = document.getElementById("lane");
const checks = document.getElementById("checks");
const score = document.getElementById("score");
const notice = document.getElementById("notice");
function update() {
 const total=checks.querySelectorAll('input[type="checkbox"]').length;
 const done=checks.querySelectorAll('input[type="checkbox"]:checked').length;
 score.textContent=`${done} / ${total} items marked present`;
 notice.textContent=done===total?'Example checklist complete. Document authenticity, content and legal sufficiency have NOT been verified.':`${total-done} example item(s) still need operator confirmation.`;
}
function render(){
 checks.replaceChildren();
 for(const [idx,text] of lanes[lane.value].entries()){
  const label=document.createElement('label');label.className='demo-check';
  const box=document.createElement('input');box.type='checkbox';box.id='check-'+idx;
  const caption=document.createElement('span');caption.textContent=text;
  label.append(box,caption);checks.append(label);box.addEventListener('change',update);
 }
 update();
}
lane.addEventListener('change',render);
document.getElementById('reset').addEventListener('click',render);
render();
