package com.project.ai;

import lombok.Data;

@Data
public class PitRecentTotalDTO {
	private int idx;
	private int code;
	private double era;
	private double kpit;
	private double kbb;
	private double wpa;
	private double re24;
	private double whip;

	//조인으로 불러오는 이름값
	private String name;
}
