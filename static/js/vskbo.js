var id = localStorage.getItem("id");
console.log(id);

$(document).ready(function() {
    // 2019년 성적 결과 호출
    show_result(id);
    make_button(id);
});

// 2019년 성적 결과 계산하여 점수 부여한 후 총점을 바탕으로 순위 계산하여 리스트 만들기
function show_result(id) {
    $.ajax({
        type: 'GET',
        url: '/api/result',
        data: {},
        success: function(response) {
            if (response['result'] == 'success') {
                console.log(response);

                // 팀 간 스탯 순위를 정하기 위한 변수
                var avg1 = [];
                var run1 = [];
                var hit1 = [];
                var hr1 = [];
                var rbi1 = [];
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
                    avg1.push(response['data'][i]["Avg"]);
                    run1.push(response['data'][i]["Run"]);
                    hit1.push(response['data'][i]["Hit"]);
                    hr1.push(response['data'][i]["Hr"]);
                    rbi1.push(response['data'][i]["RBI"]);
                }
                console.log(teams);
                function getDuplicateArrayElements(arr){
                    var sorted_arr = arr.slice().sort();
                    var results = [];
                    for (var i = 0; i < sorted_arr.length - 1; i++) {
                        if (sorted_arr[i + 1] === sorted_arr[i]) {
                            results.push(sorted_arr[i]);
                        }
                    }
                    return results;
                }
                
                var duplicaterunStat= getDuplicateArrayElements(run1);
                var duplicatehitStat= getDuplicateArrayElements(hit1);
                var duplicatehrStat= getDuplicateArrayElements(hr1);
                var duplicaterbiStat= getDuplicateArrayElements(rbi1);

                console.log(duplicaterunStat);
                if (duplicaterunStat.length !== 0){

                    function finalStat(team) {
                        return team.Run === duplicaterunStat[0];
                    }

                    // 해당 타율의 팀 index 저장
                    var index = teams.findIndex(finalStat);
                    console.log(teams[index]);
                    teams[index]["Run"] +=1;
                }

                if (duplicatehitStat.length !== 0){
                    function finalStat(team) {
                        return team.Hit === duplicatehitStat[0];
                    }

                    // 해당 타율의 팀 index 저장
                    var index = teams.findIndex(finalStat);
                    teams[index]["Hit"] +=1;
                }

                if (duplicatehrStat.length !== 0){
                    function finalStat(team) {
                        return team.Hr === duplicatehrStat[0];
                    }

                    // 해당 타율의 팀 index 저장
                    var index = teams.findIndex(finalStat);
                    teams[index]["Hr"] +=1;
                }

                if (duplicaterbiStat.length !== 0){
                    function finalStat(team) {
                        return team.RBI === duplicaterbiStat[0];
                    }

                    // 해당 타율의 팀 index 저장
                    var index = teams.findIndex(finalStat);
                    teams[index]["RBI"] +=1;
                }

                for (var i = 0; i<teams.length; i++){
                    avg.push(teams[i]["Avg"]);
                    run.push(teams[i]["Run"]);
                    hit.push(teams[i]["Hit"]);
                    hr.push(teams[i]["Hr"]);
                    rbi.push(teams[i]["RBI"]);
                }

                // 각 스탯을 올라가는 순서로 정렬한다.
                avg.sort();
                run.sort(function(a, b) {
                    return a - b
                });
                hit.sort(function(a, b) {
                    return a - b
                });
                hr.sort(function(a, b) {
                    return a - b
                });
                rbi.sort(function(a, b) {
                    return a - b
                });

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
    setTimeout(pre_delete(id), 1000);
}

function make_button(id) {
    console.log(id);
    const button = `<button type="button" class="btn btn-primary" onclick="delete_allplayer('${id}')">Play Again!</button>`;
    $('#button').append(button);
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


function pre_delete(id) {
    $.ajax({
        type: "POST",
        url: "/api/deleteall",
        data: { "id": id },
        success: function(response) {
            if (response['result'] == 'success') {;
            }
        }
    });
}
// 한 게임에 입력된 내 팀 명단을 삭제 
function delete_allplayer(id) {

    $.ajax({
        type: "POST",
        url: "/api/deleteall",
        data: { "id": id },
        success: function(response) {
            if (response['result'] == 'success') {
                alert('Go Make a New Team!');
                window.location.href = "./selectmyteam";
            }
        }
    });
}