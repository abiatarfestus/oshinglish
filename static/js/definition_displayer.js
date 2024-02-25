function displayDefinition() {
var selectedDef = document.getElementById("wordPairDefinition").value;
console.log(selectedDef);
if (selectedDef) {
    // var defIndex = selectedDef;
    var pos = definition.pos;
    var engDef = definition.eng_definition;
    var oshDef = definition.osh_definition;
    document.getElementById("pos").innerHTML = `<strong>POS:</strong> ${pos}`;
    document.getElementById("english_definition").innerHTML = `<strong>English:</strong> ${engDef}`;
    document.getElementById("oshindonga_definition").innerHTML = `<strong>Oshindonga:</strong> ${oshDef}`;
}
}