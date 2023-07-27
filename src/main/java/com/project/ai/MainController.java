package com.project.ai;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.time.LocalDate;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

import javax.servlet.ServletRequest;
import javax.servlet.http.HttpServletRequest;

import org.python.antlr.PythonParser.return_stmt_return;
import org.springframework.beans.factory.annotation.Autowired;
/*import org.springframework.core.io.ResourceLoader;*/
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;

//컨트롤러 어노테이션이 달려있는 리퀘스트 매핑을 실행한다
@Controller
public class MainController {
	
	@Autowired
	ProjectService it;
	
	//아무것도 안쓰면 메인페이지로 이동	
	@RequestMapping("/")
	public String home(ServletRequest req, LineupDTO lineupDTO, Model model) {
//		오늘날짜를 가지고 데이터 가져오기
		/* LocalDate today = LocalDate.now(); */
		LocalDateTime now = LocalDateTime.now();
//		System.out.println(now);
		/* System.out.println(today); */
		
		DateTimeFormatter formatter = DateTimeFormatter.ofPattern("HH:mm:ss");
	    String formattedDateTime = now.format(formatter);
	    String formattedTime = now.format(formatter);
//	    System.out.println(formattedTime);

		List<LineupDTO> tMatch = it.select();
		model.addAttribute("tMatch", tMatch);
		System.out.println(tMatch);
		
		if(tMatch == null || tMatch.isEmpty()) {
//			System.out.println("오늘의 경기가없습니다");
			model.addAttribute("tMatch", null);
			model.addAttribute("time", formattedTime);
			return "none";
			
		}else {
			String pythonScriptPathB = "./src/main/resources/static/vs_visualize.py";
			String pythonScriptPathK = "./src/main/resources/static/keyplayer.py";
			String[] command = null;
			String[] commandH = null;
			String[] commandA = null;
			StringBuilder output = new StringBuilder();
			StringBuilder outputH = new StringBuilder();
			StringBuilder outputA = new StringBuilder();
			
//			홈페이지에서 parameter값을 받아온다 메서드인자로 ServletRequest써야함
			String clickGame = req.getParameter("game");
//			System.out.println(clickGame);
//			처음홈페이지에 들어왔을때
			if(clickGame == null) {
//				기본값설정(첫번째 경기가 출력)
				model.addAttribute("clickGame", 1);
				
				command = new String[]{"python", pythonScriptPathB,Double.toString(tMatch.get(0).getHm_odds()),Double.toString(tMatch.get(0).getHm_getscore()),Double.toString(tMatch.get(0).getHm_conceded()),Double.toString(tMatch.get(0).getAw_odds()),Double.toString(tMatch.get(0).getAw_getscore()),Double.toString(tMatch.get(0).getAw_conceded())};
				commandH = new String[]{"python", pythonScriptPathK,Double.toString(tMatch.get(0).getKey_hm_avg()),Double.toString(tMatch.get(0).getKey_hm_slg()),Double.toString(tMatch.get(0).getKey_hm_obp())};
				commandA = new String[]{"python", pythonScriptPathK,Double.toString(tMatch.get(0).getKey_aw_avg()),Double.toString(tMatch.get(0).getKey_aw_slg()),Double.toString(tMatch.get(0).getKey_aw_obp())};
				
				try {
					Process process = Runtime.getRuntime().exec(command);
					Process processH = Runtime.getRuntime().exec(commandH);
					Process processA = Runtime.getRuntime().exec(commandA);
					BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
					BufferedReader readerH = new BufferedReader(new InputStreamReader(processH.getInputStream()));
					BufferedReader readerA = new BufferedReader(new InputStreamReader(processA.getInputStream()));
					String line;
					String lineH;
					String lineA;
					while ((line = reader.readLine()) != null ) {
			              output.append(line).append("\n");
			        }
					while ((lineH = readerH.readLine()) != null ) {
			              outputH.append(lineH).append("\n");
			        }
					while ((lineA = readerA.readLine()) != null ) {
			              outputA.append(lineA).append("\n");
			        }
					BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
					BufferedReader errorReaderH = new BufferedReader(new InputStreamReader(processH.getErrorStream()));
					BufferedReader errorReaderA = new BufferedReader(new InputStreamReader(processA.getErrorStream()));

					String errorOutput;
					String errorOutputH;
					String errorOutputA;
			        while ((errorOutput = errorReader.readLine()) != null || (errorOutputH = errorReaderH.readLine()) != null || (errorOutputA = errorReaderA.readLine()) != null) {
			              System.err.println("Error: " + errorOutput);
			        }
			        int exitCode = process.waitFor();
			        int exitCodeH = processH.waitFor();
			        int exitCodeA = processA.waitFor();
			        if (exitCode == 0 || exitCodeH == 0 || exitCodeA == 0) {
			              System.out.println("Script executed successfully");
			              model.addAttribute("pData", output.toString());
			              model.addAttribute("hData", outputH.toString());
			              model.addAttribute("aData", outputA.toString());
			          }
			          else {
			              System.out.println("Script execution failed");
			          }
				} catch (IOException | InterruptedException e) {
					 e.printStackTrace();
				}
				return "home";
			}
//			원하는 매치를 클릭했을때
			else if(clickGame != null) {
				int clicknum = Integer.parseInt(clickGame.replace("'", ""));
				model.addAttribute("clickGame", clicknum);
				
				command = new String[]{"python", pythonScriptPathB,Double.toString(tMatch.get(clicknum-1).getHm_odds()),Double.toString(tMatch.get(clicknum-1).getHm_getscore()),Double.toString(tMatch.get(clicknum-1).getHm_conceded()),Double.toString(tMatch.get(clicknum-1).getAw_odds()),Double.toString(tMatch.get(clicknum-1).getAw_getscore()),Double.toString(tMatch.get(clicknum-1).getAw_conceded())};
				commandH = new String[]{"python", pythonScriptPathK,Double.toString(tMatch.get(clicknum-1).getKey_hm_avg()),Double.toString(tMatch.get(clicknum-1).getKey_hm_slg()),Double.toString(tMatch.get(clicknum-1).getKey_hm_obp())};
				commandA = new String[]{"python", pythonScriptPathK,Double.toString(tMatch.get(clicknum-1).getKey_aw_avg()),Double.toString(tMatch.get(clicknum-1).getKey_aw_slg()),Double.toString(tMatch.get(clicknum-1).getKey_aw_obp())};
				
				try {
					Process process = Runtime.getRuntime().exec(command);
					Process processH = Runtime.getRuntime().exec(commandH);
					Process processA = Runtime.getRuntime().exec(commandA);
					BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
					BufferedReader readerH = new BufferedReader(new InputStreamReader(processH.getInputStream()));
					BufferedReader readerA = new BufferedReader(new InputStreamReader(processA.getInputStream()));
					String line;
					String lineH;
					String lineA;
					while ((line = reader.readLine()) != null ) {
			              output.append(line).append("\n");
			        }
					while ((lineH = readerH.readLine()) != null ) {
			              outputH.append(lineH).append("\n");
			        }
					while ((lineA = readerA.readLine()) != null ) {
			              outputA.append(lineA).append("\n");
			        }
					BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
			        String errorOutput;
			        while ((errorOutput = errorReader.readLine()) != null) {
			              System.err.println("Error: " + errorOutput);
			        }
			        int exitCode = process.waitFor();
			        int exitCodeH = processH.waitFor();
			        int exitCodeA = processA.waitFor();
			        if (exitCode == 0 || exitCodeH == 0 || exitCodeA == 0) {
			              System.out.println("Script executed successfully");
			              model.addAttribute("pData", output.toString());
			              model.addAttribute("hData", outputH.toString());
			              model.addAttribute("aData", outputA.toString());
			          }
			          else {
			              System.out.println("Script execution failed");
			          }
				} catch (IOException | InterruptedException e) {
					 e.printStackTrace();
				}
				return "home";
			}
			
			return "home";
		}	
		
	}
	
//	개인기록 HttpServletRequest 파라미터로 받은 값
	@RequestMapping("/info") 
	public String info(HttpServletRequest req,HitDTO hitDTO, PitDTO pitDTO, PlayerDTO playerDTO, Model model) { 
		
		if(req.getParameter("playerCode") != null) {
			int code = Integer.parseInt(req.getParameter("playerCode"));
			playerDTO.setCode(code);
			/* System.out.println(playerDTO); */
			PlayerDTO name = it.playerSelectName(playerDTO);
			
			String playerCode = "";
			String pythonScriptPathT = "./src/main/resources/static/hex_visualize.py";
			String pythonScriptPathS = "./src/main/resources/static/line_visualize.py";
			
			
			String[] command = null;
			String[] scommand = null;
			StringBuilder output = new StringBuilder();
			StringBuilder outputs = new StringBuilder();
			String position = "";
			String result = "";
			if(name.getPosition().equals("pit")) {
				List<PitDTO> pit = it.Selectpit(name);
				model.addAttribute("pit", pit);
			
				playerCode = String.valueOf(pit.get(0).getCode());
				
				position = "pit";
				PitRecentTotalDTO pTotal = it.getTotalPitData(playerCode);
//				System.out.println(pTotal);
				
				List<Pit_seasonDTO> pSeason = it.getPitSeasonData(playerCode);
				result += String.valueOf(pSeason);
//				System.out.println(result);
				if(pTotal == null || pSeason.isEmpty()) {
					return null;
				}else {
					if(pTotal != null || pSeason != null) {
						
						command = new String[]{"python", pythonScriptPathT, position,Double.toString(pTotal.getEra()), Double.toString(pTotal.getKpit()), Double.toString(pTotal.getKbb()), Double.toString(pTotal.getWpa()), Double.toString(pTotal.getRe24()), Double.toString(pTotal.getWhip()), "통산"};

						scommand = new String[]{"python", pythonScriptPathS,position ,result};
										
						try {
					          Process process = Runtime.getRuntime().exec(command);
					          Process processS = Runtime.getRuntime().exec(scommand);
					          BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
					          BufferedReader readerS = new BufferedReader(new InputStreamReader(processS.getInputStream()));
					          String line;
					          String lineS;
					          while ((line = reader.readLine()) != null ) {
					              output.append(line).append("\n");
					          }
					          while ((lineS = readerS.readLine()) != null ) {
					        	  outputs.append(lineS).append("\n");					        	  
					          }
					          BufferedReader errorReader = new BufferedReader(new InputStreamReader(processS.getErrorStream()));
					          String errorOutput;
					          while ((errorOutput = errorReader.readLine()) != null) {
					              System.err.println("Error: " + errorOutput);
					          }

					          int exitCode = process.waitFor();
					          int exitCodeS = processS.waitFor();
//					          System.out.println(exitCode);
//					          System.out.println(exitCodeS);
					          if (exitCode == 0 || exitCodeS == 0) {
					              System.out.println("Script executed successfully");
					              model.addAttribute("pData", output.toString());
					              model.addAttribute("sData", outputs.toString());
					              //System.out.println(outputs.toString().replace("==========", ""));
//					              System.out.println(outputs.toString());
					          }
					          else {
					              System.out.println("Script execution failed");
					          }
					      }
					      catch (IOException | InterruptedException e) {
					          e.printStackTrace();					          
					      }
						  return "info";
					}
				}
				
			}
			else {
				List<HitDTO> hit = it.Selecthit(name);
				model.addAttribute("hit", hit);;
				playerCode = String.valueOf(hit.get(0).getCode());
				
				position = "hit";
				HitRecentTotalDTO hTotal = it.getTotalHitData(playerCode);
//				System.out.println(hTotal);
				
				List<Hit_seasonDTO> hSeason = it.getHitSeasonData(playerCode);
				result += String.valueOf(hSeason);
//				System.out.println(result);
				
				if(hTotal == null || hSeason.isEmpty()) {
					return null;
				}else {
					if(hTotal != null || hSeason != null) {
						
						command = new String[]{"python", pythonScriptPathT, position,Double.toString(hTotal.getAvg()), Double.toString(hTotal.getSlg()), Double.toString(hTotal.getBbk()), Double.toString(hTotal.getWpa()), Double.toString(hTotal.getRe24()), Double.toString(hTotal.getObp()), "통산"};
//						System.out.println(command);
						scommand = new String[]{"python", pythonScriptPathS,position ,result};
						try {
					          Process process = Runtime.getRuntime().exec(command);
					          Process processS = Runtime.getRuntime().exec(scommand);
					          BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
					          BufferedReader readerS = new BufferedReader(new InputStreamReader(processS.getInputStream()));
					          String line;
					          String lineS;
					          while ((line = reader.readLine()) != null ) {
					              output.append(line).append("\n");
					          }
					          while ((lineS = readerS.readLine()) != null ) {
					        	  outputs.append(lineS).append("\n");
					          }
					          BufferedReader errorReader = new BufferedReader(new InputStreamReader(processS.getErrorStream()));
					          String errorOutput;
					          while ((errorOutput = errorReader.readLine()) != null) {
					              System.err.println("Error: " + errorOutput);
					          }

					          int exitCode = process.waitFor();
					          int exitCodeS = processS.waitFor();
//					          System.out.println(exitCode);
//					          System.out.println(exitCodeS);
					          if (exitCode == 0 || exitCodeS == 0) {
					              System.out.println("Script executed successfully");
					              model.addAttribute("pData", output.toString());
					              model.addAttribute("sData", outputs.toString());
//					              System.out.println(outputs.toString());
					          }
					          else {
					              System.out.println("Script execution failed");
					          }
					      }
					      catch (IOException | InterruptedException e) {
					          e.printStackTrace();					          
					      }
					}
				}
			}
		}
		return "info";
	}
	
//	개인기록에서 선수검색
	@RequestMapping("/player")
	public String player(ServletRequest req,HitDTO hitDTO, PitDTO pitDTO, PlayerDTO playerDTO, Hit_seasonDTO hit_seasonDTO, Pit_seasonDTO pit_seasonDTO ,Model model) {
		String player = req.getParameter("playerSearch");
		playerDTO.setName(player);
		//해당 이름을 가지고 code를 가져오는법		
		List<PlayerDTO> name = it.playerCodeS(playerDTO);
		
		//if해당선수가 없을때 else if해당선수가 있을때
		if(name.isEmpty()) {
//			System.out.println(name);
			model.addAttribute("no123", 123);
			return "info";
		}else if(name.size() == 1) {
			if(name.get(0).getPosition().equals("pit")) {
				List<PitDTO> pit = it.Selectpit(name.get(0));
				model.addAttribute("pit", pit);
			}else {
				List<HitDTO> hit = it.Selecthit(name.get(0));
				model.addAttribute("hit",hit);
			}
		}else {
			model.addAttribute("dname", name);
		}
		return "summid";
	}
	
//	선수별비교
	@RequestMapping("/private") 
	public String Private(ServletRequest req,HitDTO hitDTO, PitDTO pitDTO, PlayerDTO playerDTO, Model model) { 
		
		return "private"; 
	}
	
	@RequestMapping("/playerGr")
	public String playerGr(ServletRequest req,HitDTO hitDTO, PitDTO pitDTO, PlayerDTO playerDTO, Model model) {
		String player = req.getParameter("name");
		playerDTO.setName(player);
		List<PlayerDTO> Pname = it.playerCodeS(playerDTO);
		model.addAttribute("Pname", Pname);
		return "private"; 
	}
	
	
	//ajax로 파이썬 그래프 그리기
	@ResponseBody
	@RequestMapping("/pythonGraph")
	public String pythonGraph(HttpServletRequest req, HitRecentTotalDTO recentTotalDTO, PitRecentTotalDTO pitRecentTotalDTO) {
	      
	   String playerCode = req.getParameter("playerCode");
	   String firstPlayer = req.getParameter("firstPlayer");
//	   System.out.println(playerCode);
//	   System.out.println(firstPlayer);
	      
	   String pythonScriptPath = "./src/main/resources/static/hex_visualize_pre.py";
	   String[] command = null;
	   StringBuilder output = new StringBuilder();
	            
	   String position = "";
	   PitRecentTotalDTO rPD = null;
	   PitRecentTotalDTO tPD = null;
	   HitRecentTotalDTO rHD = null;
	   HitRecentTotalDTO tHD = null;
	      
	   if(firstPlayer.equals("true")) {
	      position = "pit";
	   } else if (firstPlayer.equals("false")) {
	      position = "hit";
	   }
	      
	   if(position.equals("pit")) {
	      rPD = it.getRecentPitData(playerCode);
	      tPD = it.getTotalPitData(playerCode);
	         
	   } else if (position.equals("hit")) {
	      rHD = it.getRecentHitData(playerCode);
	      tHD = it.getTotalHitData(playerCode);
	         
	   }
//	   System.out.println(playerCode);
//	   System.out.println(rPD);
//	   System.out.println(tPD);
//	   System.out.println(rHD);
//	   System.out.println(tHD);
	   
	   // 기록이 없는 선수
	   if(rPD == null && rHD == null) {
	      return null; 
	   }
	   else if (tPD == null && tHD == null) {
	      if(rPD != null) {
	         command = new String[]{"python", pythonScriptPath, position, Double.toString(rPD.getEra()), Double.toString(rPD.getKpit()), Double.toString(rPD.getKbb()), Double.toString(rPD.getWpa()), Double.toString(rPD.getRe24()), Double.toString(rPD.getWhip()), "최근"};
	      }
	      else if(rHD != null) {	    	  
	         command = new String[]{"python", pythonScriptPath, position, Double.toString(rHD.getAvg()), Double.toString(rHD.getSlg()), Double.toString(rHD.getBbk()), Double.toString(rHD.getWpa()), Double.toString(rHD.getRe24()), Double.toString(rHD.getObp()), "최근"};
	         
	      }
	      try {
	          Process process = Runtime.getRuntime().exec(command);
	          BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
	          String line;
	          while ((line = reader.readLine()) != null) {
	              output.append(line).append("\n");
	          }

	          int exitCode = process.waitFor();
//	          System.out.println(exitCode);
	          if (exitCode == 0) {
	              System.out.println("Script executed successfully");
	              
	          }
	          else {
	              System.out.println("Script execution failed");
	          }
	      }
	      catch (IOException | InterruptedException e) {
	          e.printStackTrace();
	      }
	      return output.toString();
	   }
	   else if(tPD != null) {			   
	       command = new String[]{"python", pythonScriptPath, position, Double.toString(rPD.getEra()), Double.toString(rPD.getKpit()), Double.toString(rPD.getKbb()), Double.toString(rPD.getWpa()), Double.toString(rPD.getRe24()), Double.toString(rPD.getWhip()), "최근", Double.toString(tPD.getEra()), Double.toString(tPD.getKpit()), Double.toString(tPD.getKbb()), Double.toString(tPD.getWpa()), Double.toString(tPD.getRe24()), Double.toString(tPD.getWhip()), "통산"};
	       try {
	           Process process = Runtime.getRuntime().exec(command);
	           BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
	           String line;
	           while ((line = reader.readLine()) != null) {
	               output.append(line).append("\n");
	           }
	           BufferedReader errorReader = new BufferedReader(new InputStreamReader(process.getErrorStream()));
	           String errorOutput;
	            while ((errorOutput = errorReader.readLine()) != null) {
	                System.err.println("Error: " + errorOutput);
	            }

	           int exitCode = process.waitFor();
//	           System.out.println(exitCode);
	           if (exitCode == 0) {
	               System.out.println("Script executed successfully");
//	               System.out.println(output.toString());
	           }
	           else {
	               System.out.println("Script execution failed");
	           }	    	   
	       }
	       catch (IOException | InterruptedException e) {
	           e.printStackTrace();
	       }
	       return output.toString();
	   
	   }
	   else if(tHD != null) {		  
	      command = new String[]{"python", pythonScriptPath, position, Double.toString(rHD.getAvg()), Double.toString(rHD.getSlg()), Double.toString(rHD.getBbk()), Double.toString(rHD.getWpa()), Double.toString(rHD.getRe24()), Double.toString(rHD.getObp()), "최근", Double.toString(tHD.getAvg()), Double.toString(tHD.getSlg()), Double.toString(tHD.getBbk()), Double.toString(tHD.getWpa()), Double.toString(tHD.getRe24()), Double.toString(tHD.getObp()), "통산"};
	      try {
	          Process process = Runtime.getRuntime().exec(command);
	          BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
	          String line;
	          while ((line = reader.readLine()) != null) {
	              output.append(line).append("\n");
	          }
	          int exitCode = process.waitFor();	          
	          if (exitCode == 0) {
	              System.out.println("Script executed successfully");
//	              System.out.println(output.toString());
	          }
	          else {
	              System.out.println("Script execution failed");
	          }
	      }
	      catch (IOException | InterruptedException e) {
	          e.printStackTrace();
	      }
	      return output.toString();
	  }
	  else return null;
  }

	   @ResponseBody
	   @RequestMapping("/getCode")
	   public String privateGraph(HttpServletRequest req, PlayerDTO playerDTO) {
	      String inputName = req.getParameter("inputName");      
	      playerDTO.setName(inputName);
	      List<PlayerDTO> names = it.playerCodeS(playerDTO);
	      String result = "";
//	      {"length":값, "code":[값들], "position":[값들]} 모양으로 만들어야한다.
	      
	      if(names.size()==0) {
	         result = "{\"length\":0, \"code\":[], \"position\":[]}";
	         return result;
	      }
	      else if(names.size()==1) {
	         String oneCode = String.valueOf(names.get(0).getCode());
	         String onePosition = String.valueOf(names.get(0).getPosition());
	         result = "{\"length\":1, \"code\":[" + oneCode + "], \"position\":[\"" + onePosition + "\"]}";   
//	         System.out.println(result);
	         return result;
	      }
	      else {
	         result = "{\"length\":" + names.size() + ", \"code\":[";
	         for(PlayerDTO f: names) {
	            String twoCode = String.valueOf(f.getCode());
	            result += twoCode + ",";
	         }
	         result = result.substring(0, result.length()-1) + "], \"position\":[";
	         for(PlayerDTO f: names) {
	            String twoPosition = String.valueOf(f.getPosition());
	            result += "\"" + twoPosition + "\",";
	         }
	         result = result.substring(0, result.length()-1) + "]}";
//	         System.out.println(result);
	         return result;
	      }
	   }
	   
	   public List<PlayerDTO> twoMoreCodes(PlayerDTO playerDTO) {
	      List<PlayerDTO> twoMoreCodes = it.playerCodeS(playerDTO);
	      return twoMoreCodes;
	   }
	   
	   @ResponseBody
	   @RequestMapping(value = "/drawGraph", method = RequestMethod.POST)
	   public String drawGraph(@RequestBody Map<String, Object> requestPayload, HitRecentTotalDTO hitRecentTotalDTO, PitRecentTotalDTO pitRecentTotalDTO) {
	       List<Integer> graphData = (List<Integer>) requestPayload.get("graphData");
	       String dataLength = String.valueOf(graphData.size());
			/* System.out.println(dataLength); */
	       String position = (String)requestPayload.get("position");
//	       System.out.println(graphData);
//	       System.out.println(position);
	       String hexPath = "./src/main/resources/static/hex_visualize2.py";
	       String barPath = "./src/main/resources/static/bar_visualize2.py";
	       StringBuilder hexOutput = new StringBuilder();
	       StringBuilder barOutput = new StringBuilder();
	       
	       if(dataLength.equals("0")) {
	          return "{\"length\":0}";
	       }
	       else {   
	          if(position.equals("hit")) {
	             List<HitRecentTotalDTO> HT = it.hitCompare(graphData);
	   //          System.out.println(HT);
	             String HTAsString = HT.stream()
	                       .map(HitRecentTotalDTO::toString)
	                       .collect(Collectors.joining(", "));
	   //          System.out.println(HTAsString);
	             String[] hexCommand = new String[]{"python", hexPath, position, HTAsString};
	             String[] barCommand = new String[]{"python", barPath, position, HTAsString};
	            try {
	                 Process hexProcess = Runtime.getRuntime().exec(hexCommand);
	                 Process barProcess = Runtime.getRuntime().exec(barCommand);
	                  BufferedReader hexReader = new BufferedReader(new InputStreamReader(hexProcess.getInputStream()));
	                  BufferedReader barReader = new BufferedReader(new InputStreamReader(barProcess.getInputStream()));
	                  String hexLine;
	                  String barLine;
	                  while ((hexLine = hexReader.readLine()) != null) {
	                     hexOutput.append(hexLine).append("\n");
	                  }
	                  while ((barLine = barReader.readLine()) != null) {
	                     barOutput.append(barLine).append("\n");
	                  }
	                  int hexExitCode = hexProcess.waitFor();
	                  int barExitCode = barProcess.waitFor();
	                  if (hexExitCode == 0 && barExitCode == 0) {
	                      System.out.println("Script executed successfully");
	                  }
	                  else {
	                      System.out.println("Script execution failed");
	                  }
	              }
	              catch (IOException | InterruptedException e) {
	                  e.printStackTrace();
	              }
	            return "{\"length\":" + dataLength + ", \"hex\":" + hexOutput.toString() + ", \"bar\":" + barOutput.toString() + "}";
	          }
	          else if(position.equals("pit")) {
	             List<PitRecentTotalDTO> PT = it.pitCompare(graphData);
	   //          System.out.println(PT);
	             String PTAsString = PT.stream()
	                       .map(PitRecentTotalDTO::toString)
	                       .collect(Collectors.joining(", "));
					/* System.out.println(PTAsString); */
	             String[] hexCommand = new String[]{"python", hexPath, position, PTAsString};
	             String[] barCommand = new String[]{"python", barPath, position, PTAsString};
	            try {
	                 Process hexProcess = Runtime.getRuntime().exec(hexCommand);
	                 Process barProcess = Runtime.getRuntime().exec(barCommand);
	                  BufferedReader hexReader = new BufferedReader(new InputStreamReader(hexProcess.getInputStream()));
	                  BufferedReader barReader = new BufferedReader(new InputStreamReader(barProcess.getInputStream()));
	                  String hexLine;
	                  String barLine;
	                  while ((hexLine = hexReader.readLine()) != null) {
	                     hexOutput.append(hexLine).append("\n");
	                  }
	                  while ((barLine = barReader.readLine()) != null) {
	                     barOutput.append(barLine).append("\n");
	                  }
	                  int hexExitCode = hexProcess.waitFor();
	                  int barExitCode = barProcess.waitFor();
	                  if (hexExitCode == 0 && barExitCode == 0) {
	                      System.out.println("Script executed successfully");
	                  }
	                  else {
	                      System.out.println("Script execution failed");
	                  }
	              }
	              catch (IOException | InterruptedException e) {
	                  e.printStackTrace();
	              }
	            return "{\"length\":" + dataLength + ", \"hex\":" + hexOutput.toString() + ", \"bar\":" + barOutput.toString() + "}";
	          }
	          else
	             return null;
	       }
	   }
	
	
}
