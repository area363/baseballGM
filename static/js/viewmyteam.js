var id = localStorage.getItem("id");
console.log(id);

$(document).ready(function() {
    show_myplayer(id);
    make_button(id);
    alert("Your Instance ID: " + id);
});

// 내가 선택한 선수 명단 가져오기
function show_myplayer(id) {
    $.ajax({
        type: 'POST',
        url: '/api/myteamlist',
        data: { "id": id },
        success: function(response) {
            if (response['result'] == 'success') {
                let msg = response['msg'];
                for (let i = 0; i < response['data'].length; i++) {
                    const player = response['data'][i];
                    make_list(player, i + 1);
                }
            }

        }
    });
}

function make_button(id) {
    console.log(id);
    const button = `<button type="button" onclick="finalize_team('${id}')" class="btn btn-primary">Battle with 2019 KBO League</button>`;
    $('#button').append(button);
}

// 내 선수 리스트 만들기
function make_list(player, number) {
    const card =
        `<tr>
            <th scope="row">${number}</th>
            <td>${player.Name}</td>
            <td><img height=70px width=50px src="${player.Photo}"></td>
            <td>${player.Team}</td>
            <td>${player.Position.slice(0, 3)}</td>
        </tr>`;
    $('#player-box').append(card);
}

// 내 선수단 확정해서 데이터베이스에 넣기 
function finalize_team(id) {
    $.ajax({
        type: "POST",
        url: "/api/finalteam",
        data: { "id": id },
        success: function(response) {
            if (response['result'] == 'success') {

                alert("My Team Complete!");
                window.location.href = "./vskbo";

            }
        }
    });
}