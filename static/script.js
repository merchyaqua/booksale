/* onkeyup, disable submit*/

document.querySelector("#l").onclick = function() {
    nav.style.backgroundColor = "#F7F4F3";
    br.style.color = "black";
    n.style.color = "black";
    f.style.color = "black";
    main.style.background = "white";
    nav.style.color = "black";
    main.style.color = "black";
}


function d(input1, input2) {
    if (document.querySelector(input1).value === '' && document.querySelector(input2).value === '') {
        document.querySelector('#submit').disabled = true;
    }
    else {
        document.querySelector('#submit').disabled = false;
    }
}

function d1(input1) {
    if (document.querySelector(input1).value === '') {
        document.querySelector('#submit').disabled = true;
    }
    else {
        document.querySelector('#submit').disabled = false;
    }
}

function cutie() {
    if (document.querySelector("#p").value === '') {
        document.querySelector('#submit2').disabled = true;
    }
    else {
        document.querySelector('#submit2').disabled = false;
    }
}


function forced(input1, input2) {
    if (document.querySelector(input1).value === '' || document.querySelector(input2).value === '') {
        document.querySelector('#submit').disabled = true;
    }
    else {
        document.querySelector('#submit').disabled = false;
    }
}



function forced3(input1, input2, input3) {
    if (document.querySelector(input1).value === '' || document.querySelector(input2).value === '' || document.querySelector(input3).value === '') {
        document.querySelector('#submit').disabled = true;
    }
    else if (document.querySelector(input2).value !== document.querySelector(input3).value) {
        document.querySelector('#submit').disabled = true;
    }
    else {
        document.querySelector('#submit').disabled = false;
    }
}
