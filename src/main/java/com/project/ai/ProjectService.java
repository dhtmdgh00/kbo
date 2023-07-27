package com.project.ai;

import java.util.List;

import org.apache.ibatis.annotations.Mapper;

@Mapper
public interface ProjectService {
	
	// dto의 형식을 받으려면 데이터베이스에 넣을때는 int로 한다
	public List<LineupDTO> select();
	
    // 메인페이지에서 상세보기 누르면 해당 개인기록 보여주는 메서드
	public PlayerDTO playerSelectName(PlayerDTO playerDTO);

	//	투수
	public List<PitDTO> Selectpit(PlayerDTO playerDTO);
	
	//	타자
	public List<HitDTO> Selecthit(PlayerDTO playerDTO);
	
	//개인기록 이름넣고 검색하면 데이터베이스에 이름의 코드의 리스트 가져오기
	public List<PlayerDTO> playerCodeS(PlayerDTO playerDTO);
	
	//메인페이지 그래프
	public PitRecentTotalDTO getRecentPitData(String playerCode); 
	public PitRecentTotalDTO getTotalPitData(String playerCode);
	   
	public HitRecentTotalDTO getRecentHitData(String playerCode);   
	public HitRecentTotalDTO getTotalHitData(String playerCode);
	
	//info페이지 그래프
	public List<Pit_seasonDTO> getPitSeasonData(String playerCode);
	public List<Hit_seasonDTO> getHitSeasonData(String playerCode);
	
	//private페이지
	public List<HitRecentTotalDTO> hitCompare(List<Integer> graphData);
	public List<PitRecentTotalDTO> pitCompare(List<Integer> graphData);
}
