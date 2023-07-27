<%@page import="org.apache.jasper.tagplugins.jstl.core.ForEach"%>
<%@ page language="java" contentType="text/html; charset=UTF-8"
    pageEncoding="UTF-8"%>
<%@ taglib prefix="c" uri="http://java.sun.com/jsp/jstl/core" %>
<%@ page import="java.io.File" %>
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-rbsA2VBKQhggwzxH7pPCaAqO46MgnOM80zW1RWuH61DGLwZJEdK2Kadq2F9CUG65" crossorigin="anonymous">
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="./third.css">
<title>KBO야구</title>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js"></script>
<!-- lodash cdn -->
<script src="https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.21/lodash.min.js" integrity="sha512-WFN04846sdKMIP5LKNphMaWzU7YpMyCU245etK3g/2ARYbPK9Ub18eG+ljU96qKRCWh+quCY7yefSmlkQw1ANQ==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
<script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.4/jquery.min.js"></script>
</head>
<body>
	<!-- header, nav시작 -->
	<%@ include file="../../WEB-INF/top/top.jsp" %>
	<!--<div class="container-fluid">
		<div class="container-fluid">
			<div class="container-xl">
				<header>
					<h1 class="logo">
						<a href="#">KBO 야구</a>
					</h1>
				</header>
			</div>
			<div class="container-fluid backbg">
				<div class="container-xl">
					<nav>
						<ul class="info">
							<li><a href="">오늘의 경기</a></li>
							<li><a href="#">상세보기</a></li>
							<li><a href="#">개인 기록</a></li>
						</ul>
					</nav>
				</div>
			</div>
		</div>
	</div>
	  -->
	<!-- header, nav종료 -->
	
	<!-- 메인 content 시작 -->
	<!-- 오늘의 경기 시작 -->
	<div class="container-fluid contentbg">
		<div class="container-xl">
			<div class="btngr1">
				<div class="btn-group btnpadding">
					<c:if test="${tMatch !=null}">
						<c:forEach var="tMatch" items="${tMatch}">
						  <a href="/?game='${tMatch.idx}'" class="btn btnHeight" aria-current="page" id="game1">${tMatch.teamNameK} vs ${tMatch.teamNameK2}</a>
					 	</c:forEach>
					 </c:if>
				</div>
			</div>
			<div class="btngr2">
				<ul class="vsimg">
					<li class="imglogo">
						<img src="./teamLogo/${tMatch[clickGame-1].teams_aw}.png" style="height:100px;" />
						<span>${tMatch[clickGame-1].teamNameK}</span>
					</li>
					<li class="vs">vs</li>
					<li class="imglogo">
						<img src="./teamLogo/${tMatch[clickGame-1].teams_hm}.png" style="height:100px;" />
						<span>${tMatch[clickGame-1].teamNameK2}</span>
					</li>
				</ul>
				<ul class="comparaison">
					<li>${tMatch[clickGame-1].aw_versus}</li>
					<li class="middle"> 상대전적 </li>
					<li>${tMatch[clickGame-1].hm_versus}</li>
				</ul>
				<ul class="latestGame">
					<li>${tMatch[clickGame-1].aw_winlose}</li>
					<li class="middle"> 최근경기 </li>
					<li>${tMatch[clickGame-1].hm_winlose}</li>
				</ul>
			</div>
		</div>
	</div>
	<!-- 오늘의 경기 종료 -->
	<!-- 홈/어웨이 시작 -->
	<div class="container-fluid contentbg2">
		  <div class="row gameRow">
		    <div class="col-3 gameKey">
		    	<div class="keydiv">
		    		<ul class="homeKey">
		    			<li>Key player</li>
			    		<li class="disnone">${tMatch[clickGame-1].key_aw}</li>			    		
			    		<li>
			    			<span class="font12"></span> 타 율 : ${tMatch[clickGame-1].key_aw_avg}<br>
			    			<span class="font12"></span> 장타율 : ${tMatch[clickGame-1].key_aw_slg}<br>
			    			<span class="font12"></span> 출루율 : ${tMatch[clickGame-1].key_aw_obp}<br>
			    			<span class="riggame">*최근 5경기</span>	 		    			
			    		</li>
			    		<c:set var="aDataTrimmed" value="${aData.trim()}" />
		    			<c:if test="${aDataTrimmed == 0}">
						    <li class="fontli" style="font-size:15px;">
								 <span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수는 최근 5경기에서 여러 상황에서 팀의 보탬이 되는 선수였습니다. 특히, <span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수는 타자의 대표적인 3가지 타격지표인 타율과 출루율, 장타율에서 높은 퍼포먼스를 보이며 팀의 공격력을 극대화하는 중요한 역할을 수행했습니다. 게임이 진행됨에 있어, <span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수는 출루한 선두타자를 불러들이거나 혹은 자신이 출루하여 득점할 기회를 제공 하는 등 공격에서의 윤활유 역할을 수행할 가능성이 높습니다.<br><br> 상대 투수에게 있어, <span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수는 현재 가장 주의해야 할 타자임에 틀림 없습니다. 따라서 해당 타자를 상대할때 매 투구시 집중하여 전력을 다해야 할 것입니다.														    	
						    </li>
						</c:if>
						<c:if test="${aDataTrimmed == 1}">
						    <li class="fontli" style="font-size:15px;">
								 <span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수는 최근 5경기에서 여러 상황에서 팀의 보탬이 되는 선수였습니다. 특히, <span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수는 어떠한 상황에서도 안타를 만들어 내는 능력이 매우 탁월하여 다른 지표들보다도 타율이 매우 높게 나타났습니다. <br><br> 게임이 진행됨에 있어, <span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수는 상대 투수의 압박 상황에서도 안정적으로 타격을 성공시켰으며 타석에서 활약하는 이러한 능력은 팀의 공격력을 크게 향상시킵니다.<br><br> 상대 투수는 안타능력이 탁월한 <span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수가 타석에 나오기 이전에 득점권에 주자가 출루하지 않도록 신경써야 할 것입니다.
						    	
						    </li>
						</c:if>
						<c:if test="${aDataTrimmed == 2}">
						    <li class="fontli" style="font-size:15px;">
								<span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수는 최근 5경기에서 여러 상황에서 팀의 보탬이 되는 선수였습니다. <span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수는 다른 지표들보다도 장타율이 매우 높게 나타났으며, 높은 장타율은 배트 정중앙에 볼을 맞추는 능력이 매우 탁월해 공을 멀리 보내는데 능숙한 선수라는것을 증명합니다. <br><br> 이러한 장타력은 결정적인 순간 한방이 필요한 팀과 팬들에게 강렬한 임팩트를 줄 수 있으며, 게임이 진행됨에 있어 <span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수가 경기를 이끌어 나갈 능력이 충분하다는 것을 의미합니다.<br><br> 상대 투수는 장타능력이 탁월한 <span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수가 타석에 나오기 이전에 최대한 적은 주자가 루상에 출루할 수 있는 상황을 리드해야 합니다.
						    	
						    </li>
						</c:if>
						<c:if test="${aDataTrimmed == 3}">
						    <li class="fontli" style="font-size:15px;">
								<span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수는 최근 5경기에서 여러 상황에서 팀의 보탬이 되는 선수였습니다. <span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수는 다른 지표들보다도 출루율이 매우 높게 나타났으며, 이는 <span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수가 좋은 타격감과 선구안을 겸비했다는 것을 의미합니다. 특히, <span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수는 타석에서 좋은 공과 나쁜 공을 잘 골라내 자신에게 유리한 볼카운트로 이끌어 나가는 능력이 뛰어나 상대 투수에게 압박을 가할 수 있습니다.<br><br> 득점은 출루에서부터 시작하기 때문에, <span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수는 팀 득점의 선봉장 역할을 할 가능성이 높으며 이는 팀의 공격력을 크게 향상시킬 수 있습니다.<br><br> 상대 투수는 정확한 볼 컨트롤로 유리한 볼카운트를 선점해 선구안이 뛰어난 <span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수가 출루하는 상황을 막는데 최선을 다해야합니다.
						    	
						    </li>
						</c:if>
						<c:if test="${aDataTrimmed == -1}">
						    <li class="fontli" style="font-size:15px;">
 								<span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수는 최근 5경기에서 여러 상황에서 팀의 보탬이 되는 선수였습니다. 특히, <span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수는 타자의 대표적인 지표 중 하나인 OPS를 이루는 장타율과 출루율이 매우 높게 나타나 최근 경기에서 팀 공격력에 크게 기여했습니다.<br><br> 게임이 진행됨에 있어, <span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수는 좋은 선구안을 통해 치기 힘든공은 골라내고, 실투를 캐치하여 장타를 쳐낼 수 있습니다. 만약, 득점권에 주자가 출루할 경우 어떠한 상황에서든 출루하여 주자를 홈으로 불러들여 타점을 기록할 수 있을 것입니다. 결과적으로 <span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수는 팀의 득점에 기여할 가능성이 높으며, 이는 상대 투수에게 큰 압박이 될 수 있습니다.<br><br> 상대 투수는 타격에 주축이 되는 <span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수의 약점을 사전에 정확히 파악하고, 상황에 맞게 공략하여 신중히 상대해야 할 것입니다.
						    	
						    </li>
						</c:if>
						<c:if test="${aDataTrimmed == -2}">
						    <li class="fontli" style="font-size:15px;">
								 <span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수는 최근 5경기에서 여러 상황에서 팀의 보탬이 되는 선수였습니다. 특히, <span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수는 정확한 타격 능력과 베이스를 얻어내는 능력이 뛰어나 타율과 출루율이 모두 높은 편으로 나타났습니다. <span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수의 고도화된 타격 기술과 뛰어난 선구안은 상대 투수의 체력을 소진시키는데 큰 역할을 할 수 있습니다. <br><br> 게임이 진행됨에 있어, <span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수가 이닝의 선두타자로 타석에 들 경우, 높은 출루율을 앞세워 득점을 성공할 가능성이 높기 때문에 해당 선수의 후속타자로 장타율이 높은 선수를 대타로 세우는 전략을 고려할 수 있을 것입니다.<br><br> 상대 투수는 <span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수가 출루하더라도 후속타자를 잘 잡아내어 득점으로 이어지지 않도록 최선을 다해야 합니다.
						    	
						    </li>
						</c:if>
						<c:if test="${aDataTrimmed == -3}">
						    <li class="fontli" style="font-size:15px;">
 								<span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수는 최근 5경기에서 여러 상황에서 팀의 보탬이 되는 선수였습니다. 특히, <span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수는 정확한 타격을 함과 동시에 타구를 멀리 보내는 능력을 갖추어 타율과 장타율 두 지표가 매우 높게 나타났습니다. <br><br> 게임이 진행됨에 있어, <span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수는 이러한 두 가지 능력은 루상의 주자를 홈으로 불러들일 수 있는 가능성을 크게 높이기 때문에, <span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수가 타석에 서는 것만으로 상대팀 투수에게는 큰 위협을 줄 수 있습니다.<br><br> 상대 투수는 루상에 주자가 많은 경우에 <span class="disnone">${tMatch[clickGame-1].key_aw}</span> 선수를 상대할 때, 고의사구를 통해 다음타자와 승부하는 방법을 고려해야 할 것입니다.
						    	
						    </li>
						</c:if>
			    	</ul>
		    	</div>
		    </div>
		    <!-- 테이블 시작 -->
		    <div class="col-6 gameKey">
		    	<table>
		    		<!-- 각팀 막대프래프 시작 -->
		    		<div id="bar" class="pgra">	
		    		</div>
		    		<script>
		            	if(${pData != null}) {
		            		var config = {displayModeBar: false};
		            		Plotly.purge("bar");
		            		Plotly.newPlot("bar", ${pData}.data, ${pData}.layout,config);		            			            		
		            	}
		            </script>
		            <!-- 각팀 막대프래프 종료 -->
		    		<h2 class="playinfo">어웨이 / 홈 선수 명단</h2>		    		
		    		<tbody class="infoTable">
		    			<tr>
		    				<td class="homeinfo">
								<%-- <c:if> --%>
									<div class="cards">
									<!-------------- 어웨이 팀 ---------------->
										<c:forEach var="columnName" items="${tMatch[clickGame-1].columnList_aw}">
											<div class="card">
												<div class="card__image-holder">
													<div class="card-title">
														<ul class="infoimgText">
															<li>
																<img class="card__image" src="./images/${tMatch[clickGame-1][columnName]}.jpg" />
															</li>
															<li class="infoName">
																<span class="getPlayerCode" style="display:none">${tMatch[clickGame-1][columnName]}</span>
																<span class="disnone">${tMatch[clickGame-1][columnName]}</span>
															</li>
															<li>
																<a href="javascript:void(0)" class="toggle-info btn">
																	<span class="left"></span>
																	<span class="right"></span>
																</a>
															</li>
														</ul>
													</div>   
												</div>
												<div class="card-flap flap1">
													<div class=loading id="" style="display:none">
			                                            <img src="./pront/loading.gif" alt="" style="width:150px;" />
			                                        </div>
			                                        <div class="graph" id="">                                          
			                                        </div>
													<div class="card-flap flap2">
														<div class="card-actions">
															<a href="/info?playerCode=${tMatch[clickGame-1][columnName]}" class="btn">상세보기</a>
														</div>
													</div>
												</div>
											</div>
											<c:if test="${not status.last}">
												<br />
											</c:if>
										</c:forEach>
							    	</div>
								<%-- </c:if> --%>
							</td>
		    				<td>
		    					vs
		    				</td>
		    				<td class="homeinfo">
								<div class="cards">
								<!-------------- 홈 팀 ---------------->
									<c:forEach var="columnName" items="${tMatch[clickGame-1].columnList_hm}">
										<div class="card">
											<div class="card__image-holder">
												<div class="card-title">
													<ul class="infoimgText">
														<li>
															<img class="card__image" src="./images/${tMatch[clickGame-1][columnName]}.jpg" />
														</li>
														<li class="infoName">
															<span class="getPlayerCode" style="display:none">${tMatch[clickGame-1][columnName]}</span>
															<span class="disnone">${tMatch[clickGame-1][columnName]}</span>
														</li>
														<li>
															<a href="javascript:void(0)" class="toggle-info btn">
																<span class="left"></span>
																<span class="right"></span>
															</a>
														</li>
													</ul>
												</div>   
											</div>
											<div class="card-flap flap1">
												<div class=loading id="" style="display:none">
		                                            <img src="./pront/loading.gif" alt="" style="width:150px;" />
		                                        </div>
		                                        <div class="graph" id="">                                          
		                                        </div>
												<div class="card-flap flap2">
													<div class="card-actions">
														<a href="/info?playerCode=${tMatch[clickGame-1][columnName]}" class="btn">상세보기</a>
													</div>
												</div>
											</div>
										</div>
										<c:if test="${not status.last}">
											<br />
										</c:if>
									</c:forEach>
						    	</div>
							</td>
		    			</tr>
		    		</tbody>
		    	</table>
		    </div>
		    <div class="col-3 gameKey">
		    <!-- 테이블 종료 -->
		    	<div class="keydiv">
		    		<ul class="awayKey">
		    			<li>Key player</li>
			    		<li class="disnone">${tMatch[clickGame-1].key_hm}</li>
			    		<li>
			    			<span class="font12"></span> 타 율 : ${tMatch[clickGame-1].key_hm_avg}<br>
			    			<span class="font12"></span> 장타율 : ${tMatch[clickGame-1].key_hm_slg}<br>
			    			<span class="font12"></span> 출루율 : ${tMatch[clickGame-1].key_hm_obp}<br>
			    			<span class="riggame">*최근 5경기</span>				    			
			    		</li>
			    		<c:set var="hDataTrimmed" value="${hData.trim()}" />
		    			<c:if test="${hDataTrimmed == 0}">
						    <li class="fontli" style="font-size:15px;">
								 <span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수는 최근 5경기에서 여러 상황에서 팀의 보탬이 되는 선수였습니다. 특히, <span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수는 타자의 대표적인 3가지 타격지표인 타율과 출루율, 장타율에서 높은 퍼포먼스를 보이며 팀의 공격력을 극대화하는 중요한 역할을 수행했습니다. 게임이 진행됨에 있어, <span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수는 출루한 선두타자를 불러들이거나 혹은 자신이 출루하여 득점할 기회를 제공 하는 등 공격에서의 윤활유 역할을 수행할 가능성이 높습니다.<br><br> 상대 투수에게 있어, <span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수는 현재 가장 주의해야 할 타자임에 틀림 없습니다. 따라서 해당 타자를 상대할때 매 투구시 집중하여 전력을 다해야 할 것입니다.														    	
						    </li>
						</c:if>
						<c:if test="${hDataTrimmed == 1}">
						    <li class="fontli" style="font-size:15px;">
								 <span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수는 최근 5경기에서 여러 상황에서 팀의 보탬이 되는 선수였습니다. 특히, <span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수는 어떠한 상황에서도 안타를 만들어 내는 능력이 매우 탁월하여 다른 지표들보다도 타율이 매우 높게 나타났습니다. <br><br> 게임이 진행됨에 있어, <span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수는 상대 투수의 압박 상황에서도 안정적으로 타격을 성공시켰으며 타석에서 활약하는 이러한 능력은 팀의 공격력을 크게 향상시킵니다.<br><br> 상대 투수는 안타능력이 탁월한 <span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수가 타석에 나오기 이전에 득점권에 주자가 출루하지 않도록 신경써야 할 것입니다.
						    	
						    </li>
						</c:if>
						<c:if test="${hDataTrimmed == 2}">
						    <li class="fontli" style="font-size:15px;">
								<span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수는 최근 5경기에서 여러 상황에서 팀의 보탬이 되는 선수였습니다. <span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수는 다른 지표들보다도 장타율이 매우 높게 나타났으며, 높은 장타율은 배트 정중앙에 볼을 맞추는 능력이 매우 탁월해 공을 멀리 보내는데 능숙한 선수라는것을 증명합니다. <br><br> 이러한 장타력은 결정적인 순간 한방이 필요한 팀과 팬들에게 강렬한 임팩트를 줄 수 있으며, 게임이 진행됨에 있어 <span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수가 경기를 이끌어 나갈 능력이 충분하다는 것을 의미합니다.<br><br> 상대 투수는 장타능력이 탁월한 <span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수가 타석에 나오기 이전에 최대한 적은 주자가 루상에 출루할 수 있는 상황을 리드해야 합니다.
						    	
						    </li>
						</c:if>
						<c:if test="${hDataTrimmed == 3}">
						    <li class="fontli" style="font-size:15px;">
								<span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수는 최근 5경기에서 여러 상황에서 팀의 보탬이 되는 선수였습니다. <span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수는 다른 지표들보다도 출루율이 매우 높게 나타났으며, 이는 <span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수가 좋은 타격감과 선구안을 겸비했다는 것을 의미합니다. 특히, <span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수는 타석에서 좋은 공과 나쁜 공을 잘 골라내 자신에게 유리한 볼카운트로 이끌어 나가는 능력이 뛰어나 상대 투수에게 압박을 가할 수 있습니다.<br><br> 득점은 출루에서부터 시작하기 때문에, <span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수는 팀 득점의 선봉장 역할을 할 가능성이 높으며 이는 팀의 공격력을 크게 향상시킬 수 있습니다.<br><br> 상대 투수는 정확한 볼 컨트롤로 유리한 볼카운트를 선점해 선구안이 뛰어난 <span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수가 출루하는 상황을 막는데 최선을 다해야합니다.
						    	
						    </li>
						</c:if>
						<c:if test="${hDataTrimmed == -1}">
						    <li class="fontli" style="font-size:15px;">
 								<span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수는 최근 5경기에서 여러 상황에서 팀의 보탬이 되는 선수였습니다. 특히, <span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수는 타자의 대표적인 지표 중 하나인 OPS를 이루는 장타율과 출루율이 매우 높게 나타나 최근 경기에서 팀 공격력에 크게 기여했습니다.<br><br> 게임이 진행됨에 있어, <span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수는 좋은 선구안을 통해 치기 힘든공은 골라내고, 실투를 캐치하여 장타를 쳐낼 수 있습니다. 만약, 득점권에 주자가 출루할 경우 어떠한 상황에서든 출루하여 주자를 홈으로 불러들여 타점을 기록할 수 있을 것입니다. 결과적으로 <span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수는 팀의 득점에 기여할 가능성이 높으며, 이는 상대 투수에게 큰 압박이 될 수 있습니다.<br><br> 상대 투수는 타격에 주축이 되는 <span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수의 약점을 사전에 정확히 파악하고, 상황에 맞게 공략하여 신중히 상대해야 할 것입니다.
						    	
						    </li>
						</c:if>
						<c:if test="${hDataTrimmed == -2}">
						    <li class="fontli" style="font-size:15px;">
								 <span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수는 최근 5경기에서 여러 상황에서 팀의 보탬이 되는 선수였습니다. 특히, <span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수는 정확한 타격 능력과 베이스를 얻어내는 능력이 뛰어나 타율과 출루율이 모두 높은 편으로 나타났습니다. <span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수의 고도화된 타격 기술과 뛰어난 선구안은 상대 투수의 체력을 소진시키는데 큰 역할을 할 수 있습니다. <br><br> 게임이 진행됨에 있어, <span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수가 이닝의 선두타자로 타석에 들 경우, 높은 출루율을 앞세워 득점을 성공할 가능성이 높기 때문에 해당 선수의 후속타자로 장타율이 높은 선수를 대타로 세우는 전략을 고려할 수 있을 것입니다.<br><br> 상대 투수는 <span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수가 출루하더라도 후속타자를 잘 잡아내어 득점으로 이어지지 않도록 최선을 다해야 합니다.
						    	
						    </li>
						</c:if>
						<c:if test="${hDataTrimmed == -3}">
						    <li class="fontli" style="font-size:15px;">
 								<span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수는 최근 5경기에서 여러 상황에서 팀의 보탬이 되는 선수였습니다. 특히, <span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수는 정확한 타격을 함과 동시에 타구를 멀리 보내는 능력을 갖추어 타율과 장타율 두 지표가 매우 높게 나타났습니다. <br><br> 게임이 진행됨에 있어, <span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수는 이러한 두 가지 능력은 루상의 주자를 홈으로 불러들일 수 있는 가능성을 크게 높이기 때문에, <span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수가 타석에 서는 것만으로 상대팀 투수에게는 큰 위협을 줄 수 있습니다.<br><br> 상대 투수는 루상에 주자가 많은 경우에 <span class="disnone">${tMatch[clickGame-1].key_hm}</span> 선수를 상대할 때, 고의사구를 통해 다음타자와 승부하는 방법을 고려해야 할 것입니다.
						    	
						    </li>
						</c:if>
		    		</ul>
		    		
		    	</div>
		    	<div>
		    		
		    	</div>
		    </div>
		  </div>
		</div>
		
	</div>
	<!-- 홈/어웨이 종료 -->
	<!-- 메인 content 종료 -->
	<!-- 바텀부분 시작 -->
	<div container-fluid>
		
	</div>
<script type="module">
import jsonData from '/js/codeTable.js'
const groupByData = _.groupBy(jsonData, 'code')
const nameEl = document.querySelectorAll('.disnone')

nameEl.forEach(el => {
const nameCode = el.innerText
const name = groupByData[nameCode][0]?.name
el.innerText = name
})
</script>
<script type="text/javascript">
$(document).ready(function(){
	   var zindex = 10;
	   var currentGraphDivId = null;
	   var playerCode = null;
	   var firstPlayer = false;
	   var graphs = [];
	   function addGraph(graphDivId) {
	      graphs.push(graphDivId);
	   }
	   function hasGraph(graphDivId) {
	      return graphs.includes(graphDivId);
	   };
	   
	   $(document).ajaxStart(function() {
	         $(this).find("div.loading").show();
	     });

	     $(document).ajaxStop(function() {
	        $(this).find("div.loading").hide();
	     });
	     
	   $("div.card").click(function(e){
	       var isShowing = false;

	       if ($(this).hasClass("show")) {
	         isShowing = true
	       }

	       if ($("div.cards").hasClass("showing") && !$(e.target).closest(".graph").length) {
	         // a card is already in view
	         $("div.card.show").removeClass("show");

	         if (isShowing) {
	           // this card was showing - reset the grid                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                               
	           $("div.cards").removeClass("showing");
	         } else {
	           // this card isn't showing - get in with it
	           
	            $(this)
	              .css({zIndex: zindex})
	                .addClass("show");
	            var graphDivId = $(this).find("div.graph").attr("id");
	           if (currentGraphDivId !== null) {
	              Plotly.purge(currentGraphDivId);
	             }
	           var playerCode = $(this).find("span.getPlayerCode").text();
	           firstPlayer = $(this).index() === 0;
	           var graphData = {
	                playerCode: playerCode,
	                firstPlayer: firstPlayer
	           };
	           if(!hasGraph(graphDivId)){
	              addGraph(graphDivId);
	              $.ajax({
	                  url: "/pythonGraph",
	                  contentType: "application/json; charset=utf-8",
	                  data: graphData,
	                  dataType: 'json',
	                  success: function(rData){
	                     var pythonData = rData.data;
	                     var pythonLayout = rData.layout;
	                     var config = {displayModeBar: false};
	                     Plotly.purge(graphDivId);
	                     Plotly.newPlot(graphDivId, pythonData, pythonLayout,config);
	                     graphExists = true;
	                  }, 
	                  error: function(){                  
	                  }                
	               })
	           }
	         }
	       zindex++;
	       } else {          
	         // no cards in view
	          $("div.cards")
	              .addClass("showing");
	            $(this)
	              .css({zIndex:zindex})
	              .addClass("show");
	          var graphDivId = $(this).find("div.graph").attr("id");
	           if (currentGraphDivId !== null) {
	              Plotly.purge(currentGraphDivId);
	             }
	           var playerCode = $(this).find("span.getPlayerCode").text();
	           firstPlayer = $(this).index() === 0;
	           var graphData = {
	                playerCode: playerCode,
	                firstPlayer: firstPlayer
	           };
	           if(!hasGraph(graphDivId)){
	              addGraph(graphDivId);
	              $.ajax({
	                  url: "/pythonGraph",
	                  contentType: "application/json; charset=utf-8",
	                  data: graphData,
	                  dataType: 'json',
	                  success: function(rData){
	                	 var config = {displayModeBar: false};
	                     var pythonData = rData.data;
	                     var pythonLayout = rData.layout;
	                     Plotly.purge(graphDivId);
	                     Plotly.newPlot(graphDivId, pythonData, pythonLayout,config);
	                     graphExists = true;
	                  }, 
	                  error: function(){                  
	                  }                
	               })
	           }
	            zindex++;
	       }
	       
	   });
	});

	$(document).click(function(e) {
	     var $target = $(e.target);

	     // 클릭한 요소가 "div.card"인 경우 리턴하여 아무 작업도 하지 않음
	     if ($target.closest("div.card").length > 0)
	    	 return;

	     // 열려있는 카드가 있으면 닫기
	     if ($("div.card.show").length > 0) {
	       $("div.card.show").removeClass("show");
	       $("div.cards").removeClass("showing");
	     }
	   });


  var graphElements = document.getElementsByClassName("graph");
  for (var i = 0; i < graphElements.length; i++) {
    graphElements[i].id = "graph" + (i);
  }
  var loadingElements = document.getElementsByClassName("loading");
  for (var i = 0; i < loadingElements.length; i++) {
    loadingElements[i].id = "loading" + (i);
  }
</script>
</body>
</html>