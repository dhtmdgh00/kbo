package com.project.ai;

import java.util.ArrayList;
import java.util.List;

import lombok.Data;

@Data
public class LineupDTO {
	private int idx;
	private int game_dates;
	private String teams_hm;
	private String teams_aw;
	private int pitcher_hm;
	private int pitcher_aw;
	private int hitman_hm_1;
	private int hitman_hm_2;
	private int hitman_hm_3;
	private int hitman_hm_4;
	private int hitman_hm_5;
	private int hitman_hm_6;
	private int hitman_hm_7;
	private int hitman_hm_8;
	private int hitman_hm_9;
	private int hitman_aw_1;
	private int hitman_aw_2;
	private int hitman_aw_3;
	private int hitman_aw_4;
	private int hitman_aw_5;
	private int hitman_aw_6;
	private int hitman_aw_7;
	private int hitman_aw_8;
	private int hitman_aw_9;
	private int Key_hm;
	private double Key_hm_avg;
	private double Key_hm_slg;
	private double Key_hm_obp;
	private int Key_aw;
	private double Key_aw_avg;
	private double Key_aw_slg;
	private double Key_aw_obp;
	
	private String hm_winlose;
	private String hm_versus;
	private int hm_win;
	private int hm_draw;
	private int hm_lose;
	private String aw_winlose;
	private String aw_versus;
	private int aw_win;
	private int aw_draw;
	private int aw_losw;
	private double hm_odds;
	private double hm_getscore;
	private double hm_conceded;
	private double aw_odds;
	private double aw_getscore;
	private double aw_conceded;
	
//  inner join으로 외부에서 가져온 컬럼값
	private String teamNameK;
	private String teamNameK2;
	private List<String> columnList_aw;
	private List<String> columnList_hm;
	
	
	public LineupDTO() {
		columnList_aw = new ArrayList<>();	    
		columnList_hm = new ArrayList<>();	   
		
		
		columnList_aw.add("pitcher_aw");
		columnList_aw.add("hitman_aw_1");
		columnList_aw.add("hitman_aw_2");
		columnList_aw.add("hitman_aw_3");
		columnList_aw.add("hitman_aw_4");
		columnList_aw.add("hitman_aw_5");
		columnList_aw.add("hitman_aw_6");
		columnList_aw.add("hitman_aw_7");
		columnList_aw.add("hitman_aw_8");
		columnList_aw.add("hitman_aw_9");
		
		columnList_hm.add("pitcher_hm");	    
		columnList_hm.add("hitman_hm_1");
		columnList_hm.add("hitman_hm_2");
		columnList_hm.add("hitman_hm_3");
		columnList_hm.add("hitman_hm_4");
		columnList_hm.add("hitman_hm_5");
	    columnList_hm.add("hitman_hm_6");
	    columnList_hm.add("hitman_hm_7");
	    columnList_hm.add("hitman_hm_8");
	    columnList_hm.add("hitman_hm_9");
    }
	
//	선수이름 join관련
	private int code;
	private String name;
}
