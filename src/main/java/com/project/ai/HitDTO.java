package com.project.ai;

import java.util.ArrayList;
import java.util.List;

import lombok.Data;

//롬복을 설치하고 @data를 붙이면 자동으로 getter/setter가 설정됨
@Data
public class HitDTO {
	
	private int code;
	private int idx; 
	private int year;  //년도
	private String date;  //일
	private String result;
	private int h_order; 
	private String position; //포지션 
	private int startup;
	private int pa; //타수
	private int run; //득점
	private int hit; //안타
	private int second; //이타
	private int third; //삼타
	private int homerun; //홈런
	private int luta; //루타
	private int rbi; //타점
	private int sb_s; //도루
	private int sb_f; //도실
	private int bb; //볼넷
	private int hbb; //사구
	private int ibb; //고의4구
	private int k; //삼진
	private int dp; //병실
	private int sh; //희타
	private int sf; //희비
	private double avg; //타율
	private double abp; //출루
	private double slg; //장타
	private double ops; //OPS
	private int pit; //투구수
	private double avli; //avLi
	private double re24; //re24
	private double wpa; //wpa

	//hit 리스트
	private List<String> player_hit;
	private List<String> player_hitk;
	
	public HitDTO() {
		
		player_hit = new ArrayList<>();
		player_hitk = new ArrayList<>();
		
		player_hit.add("year"); //날짜
		player_hit.add("date"); // 
		player_hit.add("position");
		player_hit.add("pa");
		player_hit.add("run");
		player_hit.add("hit");
		player_hit.add("second");
		player_hit.add("third");
		player_hit.add("homerun");
		player_hit.add("luta");
		player_hit.add("rbi");
		player_hit.add("sb_s");
		player_hit.add("sb_f");
		player_hit.add("bb");
		player_hit.add("hbb");
		player_hit.add("ibb");
		player_hit.add("k");
		player_hit.add("dp");
		player_hit.add("sh");
		player_hit.add("sf");
		player_hit.add("avg");
		player_hit.add("abp");
		player_hit.add("slg");
		player_hit.add("ops");
		player_hit.add("pit");
		player_hit.add("avli");
		player_hit.add("re24");
		player_hit.add("wpa");
		
		player_hitk.add("시즌"); //날짜
		player_hitk.add("경기일자"); // 
		player_hitk.add("포지션");
		player_hitk.add("타수");
		player_hitk.add("득점");
		player_hitk.add("안타");
		player_hitk.add("이타");
		player_hitk.add("삼타");
		player_hitk.add("홈런");
		player_hitk.add("루타");
		player_hitk.add("타점");
		player_hitk.add("도루");
		player_hitk.add("도실");
		player_hitk.add("볼넷");
		player_hitk.add("사구");
		player_hitk.add("고의4구");
		player_hitk.add("삼진");
		player_hitk.add("병실");
		player_hitk.add("희타");
		player_hitk.add("희비");
		player_hitk.add("타율");
		player_hitk.add("출루");
		player_hitk.add("장타");
		player_hitk.add("OPS");
		player_hitk.add("투구수");
		player_hitk.add("avLi");
		player_hitk.add("re24");
		player_hitk.add("wpa");
	}
}
