import time
from obs_connection import OBSConnection
from save_image import save_image_from_obs

if __name__ == "__main__":
    obs = OBSConnection()
    
    if obs.is_connected():
        print("OBS WebSocketに接続しました")
        capture_source = "source"  # ここでキャプチャソースを指定
        team_scores = {}

        try:
            counter = 0
            area = (844, 934, 930, 1000)
            while True:
                image_file_path = f"captured_image_{counter}.png"  # ファイル名にインデックスを含める
                teams, scores = save_image_from_obs(obs.ws, image_file_path, capture_source, area)
                
                # チームごとのスコアを集計
                for team, score in zip(teams, scores):
                    if team in team_scores:
                        team_scores[team] += score
                    else:
                        team_scores[team] = score

                print("現在のスコア")
                for team, total_score in team_scores.items():
                    print(f"{team}: {total_score}")

                time.sleep(1)  # 1秒待機
        
        except Exception as e:
            print(f"画像の保存または処理に失敗しました: {e}")
        finally:
            obs.disconnect()
    else:
        print("OBS WebSocketへの接続に失敗しました")
        obs.disconnect()
