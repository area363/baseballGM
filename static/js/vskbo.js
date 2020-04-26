$(document).ready(function() {
    // 2019년 성적 결과 호출
    show_result();
});

// 2019년 성적 결과 계산하여 점수 부여한 후 총점을 바탕으로 순위 계산하여 리스트 만들기
function show_result() {
    $.ajax({
        type: 'GET',
        url: '/api/result',
        data: {},
        success: function(response) {
            if (response['result'] == 'success') {
                console.log(response);

                // 팀 간 스탯 순위를 정하기 위한 변수
                var avg = [];
                var run = [];
                var hit = [];
                var hr = [];
                var rbi = [];
                var teams = [];
                teams = [];

                // 빈 변수에 해당 데이터 입력하기 
                for (let i = 0; i < response['data'].length; i++) {

                    const team = response['data'][i];
                    teams.push(team);
                    console.log(response['data'][i]);
                    avg.push(response['data'][i]["Avg"]);
                    run.push(response['data'][i]["Run"]);
                    hit.push(response['data'][i]["Hit"]);
                    hr.push(response['data'][i]["Hr"]);
                    rbi.push(response['data'][i]["RBI"]);
                }

                // 각 스탯을 올라가는 순서로 정렬한다.
                avg.sort();
                run.sort();
                hit.sort(function(a, b) {
                    return a - b
                });
                hr.sort(function(a, b) {
                    return a - b
                });
                rbi.sort();

                // 최하위 타율부터 최상위 타율까지 1점부터 11점까지 부여 
                var j = 1;
                for (var i = 0; i < teams.length; i++) {

                    // 해당 타율이 어떤 팀에 해당하는지 확인하는 함수
                    function finalStat(team) {
                        return team.Avg === avg[i];
                    }

                    // 해당 타율의 팀 index 저장
                    var index = teams.findIndex(finalStat);

                    // 해당팀에 Score를 더한다.
                    teams[index]["Score"] = 0;
                    teams[index]["Score"] += j;
                    j++;
                }

                // 최하위 득점부터 최상위 타율까지 1점부터 11점까지 부여 
                j = 1;
                for (var i = 0; i < teams.length; i++) {
                    function finalStat(team) {
                        return team.Run === run[i];
                    }
                    var index = teams.findIndex(finalStat);

                    teams[index]["Score"] += j;
                    j++;
                }

                // 최하위 안타부터 최상위 타율까지 1점부터 11점까지 부여 
                j = 1;
                for (var i = 0; i < teams.length; i++) {
                    function finalStat(team) {
                        return team.Hit === hit[i];
                    }
                    var index = teams.findIndex(finalStat);

                    teams[index]["Score"] += j;
                    j++;
                }

                // 최하위 홈런부터 최상위 타율까지 1점부터 11점까지 부여 
                j = 1;
                for (var i = 0; i < teams.length; i++) {
                    function finalStat(team) {
                        return team.Hr === hr[i];
                    }
                    var index = teams.findIndex(finalStat);

                    teams[index]["Score"] += j;
                    j++;
                }

                // 최하위 타점부터 최상위 타율까지 1점부터 11점까지 부여 
                j = 1;
                for (var i = 0; i < teams.length; i++) {
                    function finalStat(team) {
                        return team.RBI === rbi[i];
                    }
                    var index = teams.findIndex(finalStat);

                    teams[index]["Score"] += j;
                    j++;
                }


                // 점수가 부여된 팀 리스트를 점수 결과대로 순위를 정하는 함수
                function compare(a, b) {
                    const teamA = a.Score;
                    const teamB = b.Score;

                    let comparison = 0;
                    if (teamA < teamB) {
                        comparison = 1;
                    } else if (teamA > teamB) {
                        comparison = -1;
                    }
                    return comparison;
                }

                // 점수 결과대로 랭킹 정렬하기
                teams.sort(compare);

                // 랭킹대로 리스트 만들기
                for (var i = 0; i < teams.length; i++) {
                    make_card(teams[i], i + 1);
                }


            }
        }
    });
}

// 팀 성적 결과를 리스트로 만든다
function make_card(team, rank) {
    const card =
        `<tr>
            <td>${rank}</td>
            <td><img height=50px width=50px src="${team.Logo}"></td>
            <td>${team.Team}</td>
            <td>${team.Avg}</td>
            <td>${team.Hit}</td>
            <td>${team.Hr}</td>
            <td>${team.Run}</td>
            <td>${team.RBI}</td>
            <td><b>${team.Score}</b></td>
        </tr>`;
    $('#player-box').append(card);
}

// 한 게임에 입력된 내 팀 명단을 삭제 
function delete_allplayer() {

    $.ajax({
        type: "POST",
        url: "/api/deleteall",
        data: {},
        success: function(response) {
            if (response['result'] == 'success') {
                alert('팀 삭제!')
                alert(response['count'])
            }
        }
    });
}