<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ page import="java.io.File" %>
<!DOCTYPE html>
<html>
<head>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
<meta charset="UTF-8">
<link rel="stylesheet" href="./third.css">
<title>KBO야구</title>
</head>
<body>
	<!-- header, nav시작 -->
	<%@ include file="../../WEB-INF/top/top.jsp" %>
	<!-- header, nav종료 -->
	<div class="container-fluid contentbg">
		<div class="container-xl">
			<div class="btn-group btnpadding nono">
				<c:if test="${tMatch[0] eq null || tMatch == null}">
					<div class="pnodata">다음 라인업이 공개되지 않았습니다</div>
					<c:set var="time" value="${time}"/>
					<c:set var="hour" value="${time.substring(0,2)}"/>
					<c:choose>
						<c:when test="${hour lt '13'}">
							<div class="update">다음 업데이트는<br><b>13시</b> 입니다</div>
						</c:when>
						<c:when test="${hour lt '14'}">
							<div class="update">다음 업데이트는<br><b>14시</b> 입니다</div>
						</c:when>
						<c:when test="${hour lt '15'}">
							<div class="update">다음 업데이트는<br><b>15시</b> 입니다</div>
						</c:when>
						<c:when test="${hour lt '16'}">
							<div class="update">다음 업데이트는<br><b>16시</b> 입니다</div>
						</c:when>
					</c:choose>
				</c:if>
			</div>
			<div class="comment">라인업이 공개되면 페이지가 활성화됩니다</div>
		</div>
	</div>
</body>
</html>