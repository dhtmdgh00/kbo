package com.project.ai;

import lombok.Data;

@Data
public class HitRecentTotalDTO {
	private int idx;
	private int code;
	private double avg;
	private double slg;
	private double bbk;
	private double wpa;
	private double re24;
	private double obp;
	
	//조인으로 불러오는 이름값
	private String name;
}
