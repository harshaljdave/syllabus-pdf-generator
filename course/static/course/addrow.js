
var content=0;
var x = document.getElementsByName("objective"+index);
console.log(x)
var obj_num = document.getElementById("obj_num");
for (let index = 0; index < obj_num.value; index++) {
    
    // x.value = "{{objective}}"+content;
    // content++
}


var objective = 0; 
document.getElementById("add Objectives of the course").onclick = function() {
    var obj_id = ++objective
    var petCell = document.getElementById("Objectives of the course");
    var input = document.createElement("input");
    input.name = "objective"+obj_id; 
    input.type = "text";
    var br = document.createElement("br");
    petCell.appendChild(input);
    let obj_count = document.getElementById("obj_num");
    var c_obj =  parseInt(obj_count.value);
    obj_count.value = c_obj+1;
    petCell.appendChild(br);
}

var practical = 0;
document.getElementById("add Practical content").onclick = function() {
    var prac_id = ++practical;
    var petCell = document.getElementById("Practical content");
    var input = document.createElement("input");
    input.type = "text";
    input.name = "practical"+prac_id;
    var br = document.createElement("br");
    petCell.appendChild(input);
    let prac_count = document.getElementById("prac_num");
    var c_prac =  parseInt(prac_count.value);
    prac_count.value = c_prac+1;
    petCell.appendChild(br);
}

var textbook=0;
document.getElementById("add Text Book").onclick = function() {
    var text_id = ++textbook;
    var petCell = document.getElementById("Text Book");
    var input = document.createElement("input");
    input.type = "text";
    input.name = "textbook"+text_id;
    var br = document.createElement("br");
    petCell.appendChild(input);
    let text_count = document.getElementById("text_num");
    var c_text =  parseInt(text_count.value);
    text_count.value = c_text+1;
    petCell.appendChild(br);
}


var units = 0;
var index = 3;
document.getElementById("addUnit").onclick = function () {
    var unit_id = ++units;
    var add_unit = document.getElementById("units")
    var new_row = add_unit.insertRow(index);
    index++;
    var cell1 = new_row.insertCell(0)
    cell1.innerHTML = `<input type=text name=content${unit_id}>`
    var cell2 = new_row.insertCell(1)
    cell2.innerHTML = `<input type=text name=hrs${unit_id}>`
    let unit_count = document.getElementById("unit_num");
    var c_unit =  parseInt(unit_count.value);
    unit_count.value = c_unit+1;
}


var referencebook = 0;
document.getElementById("add Reference Books").onclick = function() {
    var ref_id = ++referencebook;
    var petCell = document.getElementById("Reference Books");
    var input = document.createElement("input");
    input.type = "text";
    input.name = "referencebook"+ref_id;
    var br = document.createElement("br");
    petCell.appendChild(input);
    let ref_count = document.getElementById("ref_num");
    var c_ref =  parseInt(ref_count.value);
    ref_count.value = c_ref+1;
    petCell.appendChild(br);
}

var mooc = 0;
document.getElementById("add ICT/MOOCs Reference").onclick = function() {
    var mooc_id = ++mooc;
    var petCell = document.getElementById("ICT/MOOCs Reference");
    var input = document.createElement("input");
    input.type = "text";
    input.name = "mooc"+mooc_id;
    var br = document.createElement("br");
    petCell.appendChild(input);
    let mooc_count = document.getElementById("mooc_num");
    var c_mooc =  parseInt(mooc_count.value);
    mooc_count.value = c_mooc+1;
    petCell.appendChild(br);
}


// var CO = 0;
// document.getElementById("Course Outcomes").onclick = function() {
//     var CO_id=++CO
//     var petCell = document.getElementById("Course Outcomes");
//     var input = document.createElement("input");
//     input.type = "text";
//     input_id = "CO"+CO_id;
//     var br = document.createElement("br");
//     petCell.appendChild(input);
//     petCell.appendChild(br);
// }