<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<script src="https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.21/lodash.min.js" integrity="sha512-WFN04846sdKMIP5LKNphMaWzU7YpMyCU245etK3g/2ARYbPK9Ub18eG+ljU96qKRCWh+quCY7yefSmlkQw1ANQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<title>Insert title here</title>
<link rel="stylesheet" href="./sub.css">
</head>
<body>
	<!-- header, nav시작 -->
	<%@ include file="../../WEB-INF/top/top.jsp" %>
	<!-- header, nav종료 -->
	<!-- content 부분 시작 -->
	<div class="container-fluid boxline">
		<div class="container-xl">
			<div>
				<p class="imgline">
					<c:if test="${hit != null}">
						<ul class="thumbnail">
							<li>
								<a href="/info?playerCode=${hit[0].code}">
									<img src="./images/${hit[0].code}.jpg" alt="" class="playerimg"/>
									<span class="playn">${hit[0].code}</span>									
								</a>
							</li>
							<li class="clickimg">사진을 클릭해주세요</li>
						</ul>
					</c:if>
					<c:if test="${pit != null}">
						<ul class="thumbnail">
							<li>
								<a href="/info?playerCode=${pit[0].code}">
									<img src="./images/${pit[0].code}.jpg" alt="" class="playerimg"/>
									<span class="playn">${pit[0].code}</span>
								</a>
							</li>
							<li class="clickimg">사진을 클릭해주세요</li>
						</ul>
					</c:if>
					<c:if test="${dname != null}">
						<ul class="thumbnail">
							<c:forEach var="name" items="${dname}">
								<li>
									<%-- <p>검색하신 선수가 ${name.}명입니다 검색하신 선수를 클릭해주세요</p> --%>
									<a href="./info?playerCode=${name.code}" class="aline">
										<img src="./images/${name.code}.jpg" class="playerimg"/>
										<span class="playn">${name.code}</span>										
									</a>
								</li>
							</c:forEach>
							<li class="clickimg">사진을 클릭해주세요</li>
						</ul>
					</c:if>
				</p>
			</div>
		</div>
	</div>
</body>
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
</html>