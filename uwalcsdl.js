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
    var baseURL = document.URL.substr(0,document.URL.lastIndexOf('/'));
    var unitCode = $('#unitCode').val();
    unitCode = unitCode.toUpperCase()
    window.location = baseURL+'/units/'+unitCode+'.html';
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


function insertNavbar() {
document.write('\
  <nav class="navbar navbar-inverse navbar-fixed-top" role="navigation">\
      <div class="container">\
          <!-- Brand and toggle get grouped for better mobile display -->\
          <div class="navbar-header">\
              <button type="button" class="navbar-toggle" data-toggle="collapse" data-target="#bs-example-navbar-collapse-1">\
                  <span class="sr-only">Toggle navigation</span>\
                  <span class="icon-bar"></span>\
                  <span class="icon-bar"></span>\
                  <span class="icon-bar"></span>\
              </button>\
              <a class="navbar-brand" href="index.html">UWA LCS DL</a>\
          </div>\
          <!-- Collect the nav links, forms, and other content for toggling -->\
          <div class="collapse navbar-collapse" id="bs-example-navbar-collapse-1">\
              <ul class="nav navbar-nav" id="navbar-list">\
                  <li>\
                      <a href="index.html">Find Unit</a>\
                  </li>\
                  <li>\
                      <a href="unitList.html">List Units</a>\
                  </li>\
              </ul>\
              <ul class="nav navbar-nav navbar-right">\
                  <li>\
                      <div class="dropdown">\
                          <button class="btn btn-default dropdown-toggle" type="button" id="dropdownMenu1" data-toggle="dropdown">\
                            <span class="glyphicon glyphicon-cog"></span>\
                          </button>\
                          <ul class="dropdown-menu" aria-labelledby="dropdownMenu1">\
                          <li><a href="customUnitID.html">Request Unit</a></li>\
                          <li><a href="clearShortcuts.html">Clear Shortcuts</a></li>\
                          <li role="separator" class="divider"></li>\
                          <li><a href="about.html">About</a></li>\
                          <li><a href="https://github.com/uwalcsdl/uwalcsdl.github.io">GitHub</a></li>\
                        </ul>\
                      </div>\
                  </li>\
              </ul>\
          </div>\
          <!-- /.navbar-collapse -->\
      </div>\
      <!-- /.container -->\
  </nav>\
')
}
