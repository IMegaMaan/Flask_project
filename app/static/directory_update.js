"use strict";

window.addEventListener('DOMContentLoaded', () =>{ 


  const form = document.querySelector('#form'),
        button = document.querySelector('#submit'),
        description = form.querySelector('#description'),
        nameOfDirectory = form.querySelector('#name'),
        xmlHTTP = new XMLHttpRequest();
  // не находит путь к директории
  const url = document.URL;
        //url1 = new URL( Flask.url_for('storage.directory_update', {'id':response.params.db_directories.id}), 'http://127.0.0.1:5000');
  console.log('загрузка работает_1');  
  console.log('url', url);


  // Должно происходить отображение отправленной в response формы
  //console.log(xmlHTTP.open("GET", url1, 'http://127.0.0.1:5000'), true));

  const sendJSON = (event) =>{
    event.preventDefault();
    const request = new XMLHttpRequest();
    // see documentation http://stewartpark.github.io/Flask-JSGlue/
    // const url = new URL( Flask.url_for('storage.directory_update'), 'http://127.0.0.1:5000');
    request.open("POST", url, true);
    request.setRequestHeader("Content-Type", "application/json");
    const data = {
      "name": nameOfDirectory.value, 
    "description": description.value };
    const response = JSON.stringify({
      "jsonrpc": "2.0",
      "method": "directory_view",
      "params": {'form': data}
    });
    request.send(response);
    request.addEventListener('readystatechange', () =>{
      if (request.readyState === 4 && request.status === 200) {
        console.log('Изменение директории успешно');
      } 
      
    });


  };


  button.addEventListener('click', sendJSON);


});