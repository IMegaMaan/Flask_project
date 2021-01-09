"use strict";

window.addEventListener('DOMContentLoaded', () =>{ 

    const form = document.querySelector('#form'),
          button = document.querySelector('#submit'),
          description = form.querySelector('#description'),
          nameOfDirectory = form.querySelector('#name');

    const sendJSON = (event) =>{
      event.preventDefault();
      const request = new XMLHttpRequest();
      const url = new URL( Flask.url_for('storage.create_directory'), 'http://127.0.0.1:5000');
      request.open("POST", url, true);
      request.setRequestHeader("Content-Type", "application/json");
      const data = {"name": nameOfDirectory.value, "description": description.value };
      const response = JSON.stringify({
        "jsonrpc": "2.0",
        "method": "directory_view",
        "params": {'form': data}
      });
      request.send(response);
      request.addEventListener('readystatechange', () =>{
        if (request.readyState === 4 && request.status === 200) {
          alert('Создание директории успешно');
          description.value = '';
          nameOfDirectory.value = '';
        } 
        
      });
    };

    button.addEventListener('click', sendJSON);

});