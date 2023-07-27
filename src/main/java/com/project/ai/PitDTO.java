package com.project.ai;

import java.util.ArrayList;
import java.util.List;

import lombok.Data;

@Data
public class PitDTO {
	private int code;
	private int idx;
	private int year;
	private String date;
	private String result;
	private int startup;
	private double ip;
	private int run;
	private int er;
	private int bf;
	private int ab;
	private int hit;
	private int second;
	private int third;
	private int homerun;
	private int bb;
	private int ibb;
	private int hbb;
	private int k;
	private int pit;
	private double whip;
	private double avg;
	private double obp;
	private double ops;
	private double era;
	private double avli;
	private double re24;
	private double wpa;
	private String gsc;
	private String decision;
	private String itv;
	
	//투수 기록
	private List<String> player_pit;
	private List<String> player_pitk;
	
	public PitDTO() {
		
		player_pit = new ArrayList<>();
		player_pitk = new ArrayList<>();
		
		player_pit.add("year"); //시즌
		player_pit.add("date"); //경기일자
		player_pit.add("ip"); //이닝
		player_pit.add("run"); //실점
		player_pit.add("er"); //자책
		player_pit.add("bf"); //타자
		player_pit.add("ab"); //타수
		player_pit.add("hit"); //피안타
		player_pit.add("second"); //피이타
		player_pit.add("third"); //피삼타
		player_pit.add("homerun"); //홈런
		player_pit.add("bb"); //볼넷
		player_pit.add("ibb"); //고의4구
		player_pit.add("hbb"); //사구
		player_pit.add("k"); //삼진
		player_pit.add("pit"); //투구수
		player_pit.add("whip"); //WHIP
		player_pit.add("avg"); //피타율
		player_pit.add("obp"); //피출루율
		player_pit.add("ops"); //OPS
		player_pit.add("era"); //방어율
		player_pit.add("avli"); //avLI
		player_pit.add("re24"); //RE24
		player_pit.add("wpa"); //WPA
		
		player_pitk.add("시즌"); //시즌
		player_pitk.add("경기일자"); //경기일자
		player_pitk.add("이닝"); //이닝
		player_pitk.add("실점"); //실점
		player_pitk.add("자책"); //자책
		player_pitk.add("타자"); //타자
		player_pitk.add("타수"); //타수
		player_pitk.add("피안타"); //피안타
		player_pitk.add("피이타"); //피이타
		player_pitk.add("피삼타"); //피삼타
		player_pitk.add("홈런"); //홈런
		player_pitk.add("볼넷"); //볼넷
		player_pitk.add("고의4구"); //고의4구
		player_pitk.add("사구"); //사구
		player_pitk.add("삼진"); //삼진
		player_pitk.add("투구수"); //투구수
		player_pitk.add("WHIP"); //WHIP
		player_pitk.add("피타율"); //피타율
		player_pitk.add("피출루율"); //피출루율
		player_pitk.add("OPS"); //OPS
		player_pitk.add("방어율"); //방어율
		player_pitk.add("avLI"); //avLI
		player_pitk.add("RE24"); //RE24
		player_pitk.add("WPA"); //WPA
	}
}
