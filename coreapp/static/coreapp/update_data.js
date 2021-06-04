console.log(user_list)
console.log(dash_view_url)

var arrayLength = user_list.length;

var request = new XMLHttpRequest();

for (var i = 0; i < arrayLength; i++) {
    console.log(user_list[i]);
    var url = 'https://analytics.pbl.tec.br/api/integ/gdrive/user/update/records?user_id=' + user_list[i]
    console.log(url);
    request.open("POST", url, false);
    request.send()
}

window.location.replace(dash_view_url);