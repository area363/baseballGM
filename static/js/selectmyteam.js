var clientid = Math.floor(Math.random() * 100000000000);
const id = [];
id.push(clientid);
console.log(id);
localStorage.setItem("id", id);

$(document).ready(function() {
    // index.html 로드가 완료되면 자동으로 show_player() 함수 호출

    show_player(clientid);
    make_button(clientid);
});

function show_player(clientid) {
    $.ajax({
        type: 'GET',
        url: '/api/list',
        data: {},
        success: function(response) {
            if (response['result'] == 'success') {
                let msg = response['msg'];
                for (let i = 0; i < response['data'].length; i++) {
                    const player = response['data'][i];
                    make_card(player, clientid);


                }
            }

        }
    });

}

function make_button(clientid) {
    console.log(clientid);
    const button = `<button type="button" class="btn btn-primary" onclick="checkNumber('${clientid}')">View My Team</button>`;
    $('#button').append(button);
}
// 선수 리스트를 만든다 
function make_card(player, clientid) {
    const card =
        `<tr>
    <th scope="row">${player.Rank}</th>
    <td>${player.Name}</td>
    <td><img height=70px width=50px src="${player.Photo}"></td>
    <td>${player.Team}</td>
    <td>${player.Position.slice(0, 3)}</td>
    <td>${player.Game}</td>
    <td>${player.Avg}</td>
    <td>${player.Hit}</td>
    <td>${player.Hr}</td>
    <td>${player.Run}</td>
    <td>${player.RBI}</td>
    <td><button type="button" class="btn btn-primary" onclick="pick_player('${player.Name}', '${player.Position}', '${clientid}')">Select</button></td>
    <td><button type="button" class="btn btn-primary" onclick="delete_player('${player.Name}', '${player.Position}', '${clientid}')">Cancel</button></td>
  </tr>`;
    $('#player-box').append(card);
}

//선수를 선택한다.
function pick_player(name, position, clientid) {

    // 만약 2018년도 성적에 포지션이 없다면 2019년도 로스터에 없다는 뜻이므로 alert를 띄운다.
    console.log(clientid)
    if (position == "") {
        alert('This player is not on 2019 KBO Roster!');
        return;
    }

    $.ajax({
        type: "POST",
        url: "/api/pick",
        data: {
            'name_give': name,
            'clientid': clientid
        },
        success: function(response) {
            // 선수 선택 & 업데이트 성공할 경우
            if (response['result'] == 'success') {
                alert('Picked! Number of players on your team: ' + response['count']);
                return;
            }
            // 선수가 2019년 명단에 없을 경우
            if (response['result'] == 'DNE') {
                alert('This player is not on 2019 KBO Roster!');
                return;
            }
            // 선수 8명을 이미 선택했을 경우 
            if (response['result'] === 'morethan8') {
                alert('You\'ve already picked 8 players!');
                return;
            }
            // 이미 선택한 선수일 경우 
            if (response['result'] === 'fail') {
                alert('You\'ve already picked this player!');
                return;
            }
        }
    });
    console.log(name);
}

// 선수를 삭제한다
function delete_player(name, position, clientid) {

    $.ajax({
        type: "POST",
        url: "/api/delete",
        data: {
            'name_give': name,
            'clientid': clientid
        },
        success: function(response) {
            // 선수 삭제 성공시, 취소완료와 현재 팀원 수를 알린다.
            if (response['result'] == 'success') {
                alert('Deleted From Roster! Number of players on your team: ' + response['count'])

                // 선택 선수 명단에 없을 경우 명단에 없음을 알린다/
            } else if (response['result'] == 'DNE') {
                alert('This player\'s not on your roster!')
            }
        }
    });
}

function checkNumber(clientid) {
    $.ajax({
        type: "POST",
        url: "/api/check",
        data: { 'clientid': clientid },
        success: function(response) {
            // 선수 삭제 성공시, 취소완료와 현재 팀원 수를 알린다.
            if (response['result'] == 'success') {
                alert('Good Luck!');
                window.location.href = "./viewmyteam";

                // 선택 선수 명단에 없을 경우 명단에 없음을 알린다/
            } else if (response['result'] == 'lessthan8') {
                alert('Please pick 8 players!');
            }
        }
    });
}