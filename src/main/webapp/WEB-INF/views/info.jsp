<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>KBO 야구:개인기록</title>
<link rel="stylesheet" href="./sub.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.21/lodash.min.js" integrity="sha512-WFN04846sdKMIP5LKNphMaWzU7YpMyCU245etK3g/2ARYbPK9Ub18eG+ljU96qKRCWh+quCY7yefSmlkQw1ANQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js"></script>
</head>
<body>
	<!-- header, nav시작 -->
	<%@ include file="../../WEB-INF/top/top.jsp" %>
	<!-- header, nav종료 -->
	<!-- content 부분 시작 -->
	<div class="container-fluid">
		<div class="container-xl selectline">
			<form action="player">
<!-- 				<select name="gameYear" id="gameYear" class="gamesu">
					<option value="">시즌</option>
					<option value="2023">2023시즌</option>
					<option value="2022">2022시즌</option>
					<option value="2021">2021시즌</option>
					<option value="2020">2020시즌</option>
					<option value="2019">2019시즌</option>
					<option value="2018">2018시즌</option>
				</select> -->
				<input type="text" name="playerSearch" placeholder="선수이름을 입력해주세요"/>
				<input type="submit" value="검색"/>
			</form>
			<c:set var="nocode" value="${nocode}"/>
			<%-- <c:if test="${empty nocode}">
				<form action="player">
					<input type="text" name="playerSearch" placeholder="선수이름을 입력해주세요"/>
					<input type="submit" value="검색"/>
				</form>
			</c:if> --%>
		</div>
		<div class="container-fluid boxline">
			<c:set var="null" value="${no123}"/>
			<c:if test="${not empty no123}">
				<p class="no123">해당선수는 없습니다 다시한번 확인해주세요</p>
			</c:if>
			<div class="container-xl">
				<!-------------- 선수검색 선수사진나오는 곳 ------------------->
				<div class="imageline">
					<div class="imgandgr">
						<p class="imgline">
							
							<c:if test="${hit != null}">
								<img src="./images/${hit[0].code}.jpg" alt="" class="playerimg"/>
								<span class="getPlayerCode" style="display : none">${hit[0].code}</span>
								<span class="playn">${hit[0].code}</span>
							</c:if>
							<c:if test="${pit != null}">
								<img src="./images/${pit[0].code}.jpg" alt="" class="playerimg"/>
								<span class="getPlayerCode" style="display : none">${hit[0].code}</span>
								<span class="playn">${pit[0].code}</span>
							</c:if>							
						</p>						
					</div>
					<div id="graph">					                                        
			        </div>
			        <script>		        	
			            if(${pData != null}) {
			            	var config = {displayModeBar: false};
			            	Plotly.purge("graph");
			            	Plotly.newPlot("graph", ${pData}.data, ${pData}.layout,config);		            			            		
			            }
			        </script>
				</div>
				<!-------------- 선수검색 선수그래프 나오는 곳 ------------------->
				<c:set var="sdata" value="${sData}"/>
				<c:if test="${sData != null}">
					<div class="graline">
			            <div id="graph2" class="linegraph">
			            </div>
			            <script>
			            	if(${sData != null}) {
			            		console.log(${sData});
			            		var config = {displayModeBar: false};
			            		Plotly.purge("graph2");
			            		Plotly.newPlot("graph2", ${sData}.data, ${sData}.layout,config);		            			            		
			            	}
			            </script>		            
					</div>
				</c:if>
				<c:if test="${sData == null}">
					<div>
					
					</div>
				</c:if>
				<!-------------- 선수검색 선수표 나오는 곳 ------------------->
				<c:if test="${null}">
					<div>해당 선수는 존재하지않습니다.</div>
				</c:if>
				<!-------------- 투수 표 ------------------->
				<c:if test="${pit != null }">
					<table class="tableline header_fix">					
						<tr class="infohr">
							<c:forEach var="pitk" items="${pit[0].player_pitk}" >
								<th class="infoth">${pitk}</th>
							</c:forEach>
						</tr>
						<c:forEach var="pit" items="${pit}" >
							<tr>
								<c:forEach var="pitpl" items="${pit.player_pit}" >
									<td>${pit[pitpl]}</td>
								</c:forEach>
							</tr>
						</c:forEach>
					</table>
				</c:if>
				<!-------------- 타자 표 ------------------->
				<c:if test="${hit != null }">
					<table class="tableline header_fix">					
						<tr>
							<c:forEach var="hitk" items="${hit[0].player_hitk}" >
								<th class="infoth">${hitk}</th>
							</c:forEach>
						</tr>
						<c:forEach var="hit" items="${hit}" >
							<tr>
								<c:forEach var="hitpl" items="${hit.player_hit}" >
									<td>${hit[hitpl]}</td>
								</c:forEach>
							</tr>
						</c:forEach>
					</table>
				</c:if>
			</div>
		</div>
		<!-- 동명이인일떄 보여줄 이미지 -->
		<%-- <div class="container-fluid">
			<div class="container-xl">
				<c:forEach var="name" items="${dname}">
					<p>검색하신 선수가 ${name.}명입니다 검색하신 선수를 클릭해주세요</p>
					<a href="" class="aline">
						<img src="./images/${name.code}.jpg" class="imgjpg"/>
					</a>
				</c:forEach>
			</div>
		</div> --%>
	</div>
	<!-- content 부분 종료 -->
<script type="module">
import jsonData from '/js/codeTable.js'
const groupByData = _.groupBy(jsonData, 'code')
const nameEl = document.querySelectorAll('.playn')

nameEl.forEach(el => {
const nameCode = el.innerText
const name = groupByData[nameCode][0]?.name
el.innerText = name
})
</script>
<script type="text/javascript">
/* $(document).ready(function(){
	$.ajax({
        url: "/pythonGraphinfo",
        contentType: "application/json; charset=utf-8",
        data: graphData,
        dataType: 'json',
        success: function(rData){
           var pythonData = rData.data;
           var pythonLayout = rData.layout;
           Plotly.purge(graphDivId);
           Plotly.newPlot(graphDivId, pythonData, pythonLayout);
           graphExists = true;
        }, 
        error: function(){                  
        }                
     })	
} */
</script>

</body>
</html>