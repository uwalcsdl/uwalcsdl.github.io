/*
 *
 */

function createCookie(name) {
    var expires = "";
    document.cookie = name+"="+name+expires+"; path=/";
}

function readCookie(name) {
    var nameEQ = name + "=";
    var ca = document.cookie.split(';');
    for(var i=0;i < ca.length;i++) {
        var c = ca[i];
        while (c.charAt(0)==' ') c = c.substring(1,c.length);
        if (c.indexOf(nameEQ) == 0) return c.substring(nameEQ.length,c.length);
    }
    return null;
}

function eraseCookie(name) {
    createCookie(name,"",-1);
}

function stringInList( string, list) {
    var dict = {};
    for (var i=0; i < list.length; i++){dict[list[i]]="";}
    return string in dict;
}

function unitRedirect(){
    var unitCode = $('#unitCode').val();
    window.location = '/units/'+unitCode+'.html';
    return false;
}

function getUnitShortcuts() {
    var cookies = document.cookie.split(';');
    var navbar = document.getElementById("navbar-list");
    for (var i = 0; i < cookies.length; i++) {
        var unitCode = cookies[i];
        var link = '/units/'+unitCode+'.html';
        var li = document.createElement('li');
        var a = document.createElement('a');
        a.innerHTML = unitCode;
        a.href = link;
        li.appendChild(a);
        navbar.appendChild(li);
    }
}

function addUnitShortcutButton() {
    var cookies = document.cookie.split(';');
    var unitCode = document.title;
    var button = document.createElement('button');
    button.type = 'button';
    if (stringInList(unitCode, cookies)) {
        button.setAttribute('class','btn btn-danger');
        button.setAttribute('onclick','removeUnitShortcut("'+unitCode+'")');
        button.innerHTML = 'Remove Shortcut';
    }
    else {
        button.setAttribute('class','btn btn-success');
        button.setAttribute('onclick','addUnitShortcut("'+unitCode+'")');
        button.innerHTML = 'Add Shortcut';
    }
    var pageHeader = document.getElementById('unit-title-div');
    pageHeader.appendChild(button);
}

function addUnitShortcut(unitCode) {
    createCookie(unitCode);
    document.location.reload(true);
}

function removeUnitShortcut(unitCode) {
    eraseCookie(unitCode);
    document.location.reload(true);
}