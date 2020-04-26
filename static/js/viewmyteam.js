$(document).ready(function() {
    show_player();
});

// 내가 선택한 선수 명단 가져오기
function show_player() {
    $.ajax({
        type: 'GET',
        url: '/api/myteamlist',
        data: {},
        success: function(response) {
            if (response['result'] == 'success') {
                let msg = response['msg'];
                for (let i = 0; i < response['data'].length; i++) {
                    const player = response['data'][i];
                    make_card(player, i + 1);
                }
            }

        }
    });
}

// 내 선수 리스트 만들기
function make_card(player, number) {
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
function finalize_team() {
    $.ajax({
        type: "POST",
        url: "/api/finalteam",
        data: {},
        success: function(response) {
            if (response['result'] == 'success') {

                alert("내 선수단 확정!");
                window.location.href = "./vskbo";

            }
        }
    });
}