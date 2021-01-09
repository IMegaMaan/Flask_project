"use strict";
// законченный скрипт для создания директории



document.addEventListener('DOMContentLoader', ()=>{


    const response_type = response;
    console.log(response_type);
    console.log('Загрузка');
    const form = document.querySelector('#form'),
          username = form.querySelector('#inputEmail'),
          password = form.querySelector('#inputPassword'),
          button = form.querySelector('#submit'),
          checkbox = form.querySelector('#checkbox');


    const sendJSON = (event) =>{
      //event.preventDefault();
      const xhr = new XMLHttpRequest(),
            url = new URL( Flask.url_for('authentication.login'), 'http://127.0.0.1:5000'),
            urlToDirectories = new URL( Flask.url_for('storage.directories'), 'http://127.0.0.1:5000'),
            data = [{"name": username.value, "password": password.value , 'checkbox': checkbox.checked}],
            request = JSON.stringify({
                "jsonrpc": "2.0",
                "method": "login",
                "params": data
            });
      xhr.open("POST", url, true);
      xhr.setRequestHeader("Content-Type", "application/json");
      xhr.send(request);
      //location.reload()
      // перенаправление на страничку
      //window.location = urlToDirectories;
    };

    button.addEventListener('click', sendJSON);
});
