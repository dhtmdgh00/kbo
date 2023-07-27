<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>
<link rel="stylesheet" href="./sub.css">
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js"></script>
<script>
   var graphData = [];
   
   document.addEventListener("DOMContentLoaded", function() {
	   document.getElementById("name").addEventListener("keyup", function(event) {
	      if (event.key === "Enter") {
	         nameInput();
	       }
	   });
   });
   
   function drawGraph(){
      $.ajax({
           url: "/drawGraph",
           contentType: "application/json; charset=utf-8",
           type: "POST",
           data: JSON.stringify({
              graphData: graphData,
              position: sessionStorage.getItem("recentPosition")
           }),
           dataType: 'json',
           success: function(rData){
               console.log(rData);
               if(rData.length == 0){
                  Plotly.purge(hexGraph);
                   Plotly.purge(barGraph);
               }
               else{
                   var hexData = rData.hex.data;
                   var hexLayout = rData.hex.layout;
                   var barData = rData.bar.data;
                   var barLayout = rData.bar.layout;
                   /* console.log(hexData); */
                   Plotly.purge(hexGraph);
                   Plotly.purge(barGraph);
                   var config = {displayModeBar: false};
                   Plotly.newPlot(hexGraph, hexData, hexLayout, config);
                   Plotly.newPlot(barGraph, barData, barLayout, config);
               }
             }, 
            error: function(){                  
            }                
         })      
   }
   
   //선수 코드가 있는 버튼 생성
   function nameInput() {      
      var inputName = document.getElementById("name").value;
      // 선수 데이터가 이미 3개 있다면 오류메세지 출력
      if(document.getElementById("button1") != null
            && document.getElementById("button2") != null
            && document.getElementById("button3") != null){
         alert("선수 정보를 더 이상 추가할 수 없습니다.")
      }
      // 선수 데이터가 3개 미만일 경우 버튼 생성
      else{
         $.ajax({
              url: "/getCode",
              contentType: "application/json; charset=utf-8",
              data: {
                 inputName : inputName
              },
              dataType: 'json',
              success: function(rData){   
                 //응답값이 0개라면
                 if(rData.length == "0"){
                    alert("해당 선수는 존재하지 않습니다.");
                 }
                 //응답값이 1개라면
                 //중복 데이터가 없다면 버튼생성. 있다면 오류메세지 출력
                 else if(rData.length == 1){
                    var button1 = document.getElementById("button1");
                    var button2 = document.getElementById("button2");
                    var button3 = document.getElementById("button3");                    
                    var code1 = null; var position1 = null;
                    var code2 = null; var position2 = null;
                    var code3 = null; var position3 = null;
                    if(button1 != null){
                       code1 = button1.getAttribute("data-code");
                       position1 = button1.getAttribute("data-position");
                       console.log(position1);
                    }
                    if(button2 != null){
                       code2 = button2.getAttribute("data-code");
                       position2 = button2.getAttribute("data-position");
                       console.log(position2);
                    }
                    if(button3 != null){
                       code3 = button3.getAttribute("data-code");
                       position3 = button3.getAttribute("data-position");
                       console.log(position3);
                    }
                    if((button1 == null && button2 == null && button3 == null)
                          || (position1 == rData.position[0] || position2 == rData.position[0] || position3 == rData.position[0])){
                       if(rData.code[0] != code1 && rData.code[0] != code2 && rData.code[0] != code3){
                          var buttons = [
                              document.getElementById("button1"),
                              document.getElementById("button2"),
                              document.getElementById("button3")
                          ];
                          var buttonContainer = document.getElementById("buttonContainer");

                          for (var i = 0; i < buttons.length; i++) {
                              if (!buttons[i]) {
                                 buttons[i] = document.createElement("button");
                                  buttons[i].id = "button" + (i + 1);
                                  buttons[i].innerText = inputName;
                                  buttons[i].onclick = function() {
                                     sessionStorage.setItem("saveID", this.id);
                                 };
                                 buttons[i].dataset.code = rData.code[0];
                                 buttons[i].dataset.position = rData.position[0];
                                 document.getElementById("name").value = null;
                                 document.getElementById("name").focus();
                                 sessionStorage.setItem("recentPosition", rData.position[0]);
                                 buttonContainer.appendChild(buttons[i]);
                                 graphData.push(rData.code[0]);
                                 console.log(graphData);
                                 drawGraph();
                                 break;
                             }
                          }
                       }
                       else{
                          alert("기존에 존재하는 선수 데이터입니다.")
                       }
                    }
                    else{
                       alert("같은 포지션의 선수들만 비교가 가능합니다.")
                    }
                 }
                 //응답값이 2개 이상(동명이인)이라면 모달창을 통해 해당 선수들의 사진을 출력
                 else{                	
                     var modal = document.createElement("div");
                     modal.className = "modal";
                     modal.id = "modalPage"
                     var modalContent = document.createElement("div");
                     modalContent.className = "modal-content";
                     modalContent.id = "modalIn"

                     for (const code of rData.code) {
                        const position = rData.position[rData.code.indexOf(code)];   
                        var img = document.createElement("img");
                        //사진 클릭시 해당 사진의 선수의 버튼을 생성하고 모달창을 닫음
                        img.onclick = function() {
                           nameInput2(inputName, code, position);
                           modal.style.display = "none";
                        }
                        img.src = "./images/" + code + ".jpg";
                        img.style.width = "200px";
                        img.style.marginRight = "20px";
                        modalContent.appendChild(img);
                     }
                     modal.appendChild(modalContent);
                     document.body.appendChild(modal);
                 }               
               }, 
               error: function(){               
               }                
            })         
      }
   }
   
   //동명이인일 경우 사진을 클릭하여 해당 선수 코드를 가진 버튼 생성
   function nameInput2(inputName, code, position){
      var button1 = document.getElementById("button1");
      var button2 = document.getElementById("button2");
      var button3 = document.getElementById("button3");   
      var code1 = null; var position1 = null;
      var code2 = null; var position2 = null;
      var code3 = null; var position3 = null;
      if(button1 != null){
         code1 = button1.getAttribute("data-code");
         position1 = button1.getAttribute("data-position");
         console.log(position1);
      }
      if(button2 != null){
         code2 = button2.getAttribute("data-code");
         position2 = button2.getAttribute("data-position");
         console.log(position2);
      }
      if(button3 != null){
         code3 = button3.getAttribute("data-code");
         position3 = button3.getAttribute("data-position");
         console.log(position3);
      }
      if((button1 == null && button2 == null && button3 == null)
            || (position1 == position || position2 == position || position3 == position)){
         if(code != code1 && code != code2 && code != code3){
            var buttons = [
                document.getElementById("button1"),
                document.getElementById("button2"),
                document.getElementById("button3")
            ];
            var buttonContainer = document.getElementById("buttonContainer");

            for (var i = 0; i < buttons.length; i++) {
                if (!buttons[i]) {
                   buttons[i] = document.createElement("button");
                    buttons[i].id = "button" + (i + 1);
                    buttons[i].innerText = inputName;
                    buttons[i].onclick = function() {
                    sessionStorage.setItem("saveID", this.id);
                   };
                   buttons[i].dataset.code = code;
                   buttons[i].dataset.position = position;
                   document.getElementById("name").value = null;
                   document.getElementById("name").focus();
                   sessionStorage.setItem("recentPosition", position);
                   buttonContainer.appendChild(buttons[i]);
                   graphData.push(code);
                   console.log(graphData);
                   drawGraph();
                   break;
               }
            }
         }
         else{
            alert("기존에 존재하는 선수 데이터입니다.");
         }
      }
      else{
         alert("같은 포지션의 선수들만 비교가 가능합니다.")
      }
   }
   
   function nameDelete(){
      var saveID = sessionStorage.getItem("saveID");
      if(saveID){
         var button = document.getElementById(saveID);
         var code = button.getAttribute("data-code");
         button.parentNode.removeChild(button);
         graphData.splice(graphData.indexOf(parseInt(code)), 1);
         sessionStorage.removeItem("saveID");
         console.log(graphData);
         drawGraph();
      }
   }
   
   window.addEventListener("click", function(event) {      
      var modalPage = document.getElementById("modalPage");
      var modal = document.getElementById("modalIn");
      if (modal && event.target !== modal) {
         modalPage.parentNode.removeChild(modalPage);
       }
   });
</script>
</head>
<body>
   <!-- header, nav시작 -->
   <%@ include file="../../WEB-INF/top/top.jsp" %>
   <!-- header, nav종료 -->
   <!-- content 부분 시작 -->
   <div class="container-fluid contentbg">
      <div class="container-xl">
         <div class="make">
            <input type="text" name="name" class="name" id="name" placeholder="선수 이름을 입력하세요" />
            <button type="button" onclick="nameInput();" class="btnbord">추가</button>
            <button type="button" onclick="nameDelete();" class="btnbord">제거</button>
         </div>
         
         <!-- 위치 조절하고 이 주석 삭제 -->
         <br /><br />
         <div class="flexgra">
         	<div id="buttonContainer"></div>
         	<div class="graph" id="hexGraph"></div>
         </div>
         <div class="graph" id="barGraph"></div>
      </div>
   </div>
   <!-- content 부분 시작 -->
</body>
</html>