$(document).ready(function () {
    $('#orders-box').html('');
    listing();
});

function order() {
    // name quantity address telelphone의 값을 가져온다
    const name = $('#name').val();
    const quantity = $('#quantity').val();
    const address = $('#address').val();
    const telephone = $('#telephone').val();
    console.log(name);
    console.log(quantity);
    console.log(address);
    console.log(telephone);

    // 이름을 입력하지 않을 경우 alert
    if (name.length === 0) {
        alert("성함을 입력해주세요!");
        $('#name').focus();
        return;
    }
    // 수량을 선택하지 않을 경우 alert    
    if (quantity.length !== 1) {
        alert("수량을 선택해주세요!");
        $('#quantity').focus();
        return;
    }
    // 주소를 입력하지 않을 경우 alert
    if (address.length === 0) {
        alert("주소를 입력해주세요!");
        $('#address').focus();
        return;
    }
    // 전화번호에 "-"이 없을경우 alert
    if (telephone.indexOf("-") === -1) {
        alert("올바른 전화번호를 입력해주세요! (ex. 000-0000-0000)");
        $('#telephone').focus();
        return;
        // 모든 정보가 입력됐을 경우 주문완료 표시 & 밑섹션에 명단 추가
    }
    // POST /orders 에 저장을 요청합니다.
    $.ajax({
        type: 'POST', // 타입을 작성합니다.
        url: '/orders', // url을 작성합니다.
        data: {
            "name": name,
            "quantity": quantity,
            "address": address,
            "telephone": telephone
        }, // data를 작성합니다. },
        success: function (response) {
            if (response['result'] == 'success') {
                alert(response['msg']);
                window.location.reload();
            }
        }
    });
}

function listing() {

    // 1. 주문 목록을 서버에 요청하기
    // 2. 요청 성공 여부 확인하기
    // 3. 요청 성공했을 때 리뷰를 올바르게 화면에 나타내기
    $.ajax({
        type: "GET",
        url: "/orders",
        data: {},
        success: function (response) {
            if (response['result'] == 'success') {
                //alert(response['msg']);
                // 2. 성공했을 때 리뷰를 올바르게 화면에 나타내기
                const orders = response["orders"]

                for (let i = 0; i < orders.length; i++) {
                    let name = orders[i]["name"];
                    let quantity = orders[i]["quantity"];
                    let address = orders[i]["address"];
                    let telephone = orders[i]["telephone"];

                    make_card(name, quantity, address, telephone);
                }
            } else {
                alert('리뷰를 받아오지 못했습니다');
            }
        }
    });


}

function make_card(name, quantity, address, telephone) {

    // name, quantity, address, telephone값을 받아와 테이블 형식에 맞춰서 temp_html에 저장
    let temp_html = '<tr>\
        <td>'+ name + '</td>\
        <td>'+ quantity + '</td>\
        <td>'+ address + '</td>\
        <td>'+ telephone + '</td>\
        </tr>';

    // temp_html을 orders-box에 추가
    $('#orders-box').append(temp_html);
}

