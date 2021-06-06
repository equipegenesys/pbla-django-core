// console.log(user_list)
// console.log(dash_view_url)

var arrayLength = user_list.length;

var request = new XMLHttpRequest();

// var cookieEquipe = document.cookie.match(/^(.*;)?\s*6T9J\s*=\s*[^;]+(.*)?$/);

const regex = new RegExp(`^(.*;)?\s*${tag_equipe}\s*=\s*[^;]+(.*)?$`);

var cookieEquipe = document.cookie.match(regex);

// console.log(cookieEquipe)

if (cookieEquipe === null) {

    for (var i = 0; i < arrayLength; i++) {
        // console.log(user_list[i]);
        var url = 'https://analytics.pbl.tec.br/api/integ/gdrive/user/update/records?user_id=' + user_list[i]
        console.log(url);
        request.open("POST", url, false);
        request.send()
    }

    document.cookie = tag_equipe + "=yes";
    window.location.replace(dash_view_url);
} else {
    window.location.replace(dash_view_url);
}