import cv2
import numpy as np
import datetime
import os

# グローバル変数としてパラメータを定義
params = {
    'ycrcb_min_y': 0,
    'ycrcb_min_cr': 138,
    'ycrcb_min_cb': 85,
    'ycrcb_max_y': 255,
    'ycrcb_max_cr': 173,
    'ycrcb_max_cb': 133,
    'hsv_min_h': 0,
    'hsv_min_s': 20,
    'hsv_min_v': 80,
    'hsv_max_h': 20,
    'hsv_max_s': 150,
    'hsv_max_v': 255,
    'min_area': 1000,
    'morph_close': 2,
    'morph_open': 1
}

# トラックバーのコールバック関数
def on_trackbar(val):
    pass

def create_parameter_window():
    cv2.namedWindow('Parameters', cv2.WINDOW_NORMAL)
    cv2.resizeWindow('Parameters', 600, 700)
    
    # YCrCb パラメータ用トラックバー
    cv2.createTrackbar('YCrCb Min Y', 'Parameters', params['ycrcb_min_y'], 255, on_trackbar)
    cv2.createTrackbar('YCrCb Min Cr', 'Parameters', params['ycrcb_min_cr'], 255, on_trackbar)
    cv2.createTrackbar('YCrCb Min Cb', 'Parameters', params['ycrcb_min_cb'], 255, on_trackbar)
    cv2.createTrackbar('YCrCb Max Y', 'Parameters', params['ycrcb_max_y'], 255, on_trackbar)
    cv2.createTrackbar('YCrCb Max Cr', 'Parameters', params['ycrcb_max_cr'], 255, on_trackbar)
    cv2.createTrackbar('YCrCb Max Cb', 'Parameters', params['ycrcb_max_cb'], 255, on_trackbar)
    
    # HSV パラメータ用トラックバー
    cv2.createTrackbar('HSV Min H', 'Parameters', params['hsv_min_h'], 180, on_trackbar)
    cv2.createTrackbar('HSV Min S', 'Parameters', params['hsv_min_s'], 255, on_trackbar)
    cv2.createTrackbar('HSV Min V', 'Parameters', params['hsv_min_v'], 255, on_trackbar)
    cv2.createTrackbar('HSV Max H', 'Parameters', params['hsv_max_h'], 180, on_trackbar)
    cv2.createTrackbar('HSV Max S', 'Parameters', params['hsv_max_s'], 255, on_trackbar)
    cv2.createTrackbar('HSV Max V', 'Parameters', params['hsv_max_v'], 255, on_trackbar)
    
    # その他のパラメータ用トラックバー
    cv2.createTrackbar('Min Area (x100)', 'Parameters', params['min_area'] // 100, 100, on_trackbar)
    cv2.createTrackbar('Morph Close Iter', 'Parameters', params['morph_close'], 10, on_trackbar)
    cv2.createTrackbar('Morph Open Iter', 'Parameters', params['morph_open'], 10, on_trackbar)

def update_params_from_trackbars():
    params['ycrcb_min_y'] = cv2.getTrackbarPos('YCrCb Min Y', 'Parameters')
    params['ycrcb_min_cr'] = cv2.getTrackbarPos('YCrCb Min Cr', 'Parameters')
    params['ycrcb_min_cb'] = cv2.getTrackbarPos('YCrCb Min Cb', 'Parameters')
    params['ycrcb_max_y'] = cv2.getTrackbarPos('YCrCb Max Y', 'Parameters')
    params['ycrcb_max_cr'] = cv2.getTrackbarPos('YCrCb Max Cr', 'Parameters')
    params['ycrcb_max_cb'] = cv2.getTrackbarPos('YCrCb Max Cb', 'Parameters')
    
    params['hsv_min_h'] = cv2.getTrackbarPos('HSV Min H', 'Parameters')
    params['hsv_min_s'] = cv2.getTrackbarPos('HSV Min S', 'Parameters')
    params['hsv_min_v'] = cv2.getTrackbarPos('HSV Min V', 'Parameters')
    params['hsv_max_h'] = cv2.getTrackbarPos('HSV Max H', 'Parameters')
    params['hsv_max_s'] = cv2.getTrackbarPos('HSV Max S', 'Parameters')
    params['hsv_max_v'] = cv2.getTrackbarPos('HSV Max V', 'Parameters')
    
    params['min_area'] = cv2.getTrackbarPos('Min Area (x100)', 'Parameters') * 100
    params['morph_close'] = cv2.getTrackbarPos('Morph Close Iter', 'Parameters')
    params['morph_open'] = cv2.getTrackbarPos('Morph Open Iter', 'Parameters')

def save_params(filename="skin_params.txt"):
    with open(filename, 'w') as f:
        for key, value in params.items():
            f.write(f"{key}={value}\n")
    print(f"Parameters saved to {filename}")

def load_params(filename="skin_params.txt"):
    try:
        with open(filename, 'r') as f:
            for line in f:
                if '=' in line:
                    key, value = line.strip().split('=')
                    if key in params:
                        params[key] = int(value)
        print(f"Parameters loaded from {filename}")
        return True
    except FileNotFoundError:
        print(f"Parameter file {filename} not found")
        return False

def detect_skin(image):
    # 画像の前処理（ノイズ軽減とコントラスト調整）
    blurred = cv2.GaussianBlur(image, (3, 3), 0)
    lab_image = cv2.cvtColor(blurred, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab_image)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
    cl = clahe.apply(l)
    enhanced_lab = cv2.merge((cl, a, b))
    enhanced_image = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)
    
    # 複数の色空間を使用
    ycrcb_image = cv2.cvtColor(enhanced_image, cv2.COLOR_BGR2YCrCb)
    hsv_image = cv2.cvtColor(enhanced_image, cv2.COLOR_BGR2HSV)
    
    # パラメータから肌色範囲を設定
    lower_skin_ycrcb = np.array([params['ycrcb_min_y'], params['ycrcb_min_cr'], params['ycrcb_min_cb']], dtype=np.uint8)
    upper_skin_ycrcb = np.array([params['ycrcb_max_y'], params['ycrcb_max_cr'], params['ycrcb_max_cb']], dtype=np.uint8)
    
    lower_skin_hsv = np.array([params['hsv_min_h'], params['hsv_min_s'], params['hsv_min_v']], dtype=np.uint8)
    upper_skin_hsv = np.array([params['hsv_max_h'], params['hsv_max_s'], params['hsv_max_v']], dtype=np.uint8)
    
    # 第二のHSV範囲（赤色の循環的な性質を考慮）
    lower_skin_hsv2 = np.array([170, params['hsv_min_s'], params['hsv_min_v']], dtype=np.uint8)
    upper_skin_hsv2 = np.array([180, params['hsv_max_s'], params['hsv_max_v']], dtype=np.uint8)
    
    # マスクの作成
    mask_ycrcb = cv2.inRange(ycrcb_image, lower_skin_ycrcb, upper_skin_ycrcb)
    mask_hsv1 = cv2.inRange(hsv_image, lower_skin_hsv, upper_skin_hsv)
    mask_hsv2 = cv2.inRange(hsv_image, lower_skin_hsv2, upper_skin_hsv2)
    mask_hsv = cv2.bitwise_or(mask_hsv1, mask_hsv2)
    
    # マスクの組み合わせ（論理積と論理和を適切に組み合わせる）
    skin_mask = cv2.bitwise_and(mask_ycrcb, mask_hsv)
    
    # ノイズ処理とマスクの改善
    skin_mask = cv2.medianBlur(skin_mask, 5)
    
    # 連続した処理でマスクを改善
    kernel_ellipse = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    kernel_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    
    # クローズ処理で小さな穴を埋める
    skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_CLOSE, kernel_ellipse, iterations=params['morph_close'])
    
    # オープン処理で小さなノイズを除去
    skin_mask = cv2.morphologyEx(skin_mask, cv2.MORPH_OPEN, kernel_rect, iterations=params['morph_open'])
    
    # 輪郭検出と面積フィルタリング
    contours, _ = cv2.findContours(skin_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # 新しい空のマスクを作成
    filtered_mask = np.zeros_like(skin_mask)
    
    # 面積が最小値より大きい輪郭だけを保持
    for contour in contours:
        area = cv2.contourArea(contour)
        if area > params['min_area']:
            cv2.drawContours(filtered_mask, [contour], -1, 255, -1)
    
    # 穴を埋める
    filtered_mask = cv2.morphologyEx(filtered_mask, cv2.MORPH_CLOSE, kernel_ellipse, iterations=3)
    
    # 元の画像と最終マスクを合成
    skin_only = cv2.bitwise_and(image, image, mask=filtered_mask)
    
    # 肌色部分をさらに強調（オプション）
    skin_enhanced = skin_only.copy()
    if np.any(filtered_mask > 0):  # マスクが空でない場合のみ処理
        skin_enhanced[filtered_mask > 0] = cv2.addWeighted(
            skin_only[filtered_mask > 0], 1.2, 
            np.zeros_like(skin_only[filtered_mask > 0]), 0, 5
        )[0]
    
    # デバッグ用: 各色空間のマスクも返す
    debug_masks = {
        'ycrcb': mask_ycrcb,
        'hsv': mask_hsv,
        'combined': skin_mask,
        'filtered': filtered_mask
    }
    
    return skin_enhanced, filtered_mask, debug_masks

def main():
    # 出力ディレクトリの作成
    output_dir = "skin_detection_results"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # ウェブカメラからのキャプチャを開始
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Cannot access camera")
        return
    
    # 設定ウィンドウは初期状態では非表示
    param_window_visible = False
    
    print("Camera started. Press space to capture image.")
    print("Press 'r' to toggle parameter window.")
    print("Press 's' to save parameters.")
    print("Press 'l' to load parameters.")
    print("Press 'd' to toggle debug mode.")
    print("Press 'q' to quit.")
    
    # デバッグモード
    debug_mode = False
    
    while True:
        # フレームをキャプチャ
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Failed to capture frame")
            break
        
        # パラメータウィンドウが表示されている場合、値を更新
        if param_window_visible:
            update_params_from_trackbars()
        
        # 肌色検出処理
        try:
            preview_skin, preview_mask, debug_masks = detect_skin(frame)
            
            # 元画像、肌色抽出結果、マスクを横に並べる
            mask_colored = cv2.cvtColor(preview_mask, cv2.COLOR_GRAY2BGR)
            preview = np.hstack([frame, preview_skin, mask_colored])
            
            # リサイズ（必要な場合）
            h, w = preview.shape[:2]
            max_width = 1280
            if w > max_width:
                scale = max_width / w
                preview = cv2.resize(preview, None, fx=scale, fy=scale)
            
            # 表示
            cv2.imshow('Skin Detection', preview)
            
            # デバッグモード
            if debug_mode:
                for name, mask in debug_masks.items():
                    cv2.imshow(f'Mask: {name}', mask)
        
        except Exception as e:
            print(f"Error: {e}")
            cv2.imshow('Camera', frame)
        
        # キー入力待機
        key = cv2.waitKey(1) & 0xFF
        
        # スペースキー: 撮影
        if key == ord(' '):
            captured_image = frame.copy()
            try:
                processed_image, skin_mask, _ = detect_skin(captured_image)
                
                # 表示
                cv2.imshow('Captured', captured_image)
                cv2.imshow('Result', processed_image)
                
                # 3枚を並べた画像を作成
                mask_colored = cv2.cvtColor(skin_mask, cv2.COLOR_GRAY2BGR)
                combined_image = np.hstack([captured_image, processed_image, mask_colored])
                
                # ファイル名（年月日時間）
                now = datetime.datetime.now()
                filename = now.strftime("%Y%m%d_%H%M%S")
                
                # 保存
                output_path = os.path.join(output_dir, f'{filename}.png')
                cv2.imwrite(output_path, combined_image)
                print(f"Image saved: {output_path}")
                
                # 個別の画像も保存
                cv2.imwrite(os.path.join(output_dir, f'{filename}_original.png'), captured_image)
                cv2.imwrite(os.path.join(output_dir, f'{filename}_skin.png'), processed_image)
                cv2.imwrite(os.path.join(output_dir, f'{filename}_mask.png'), skin_mask)
                
            except Exception as e:
                print(f"Image processing error: {e}")
        
        # 'r': パラメータウィンドウ
        elif key == ord('r'):
            param_window_visible = not param_window_visible
            if param_window_visible:
                create_parameter_window()
                print("Parameter window opened")
            else:
                cv2.destroyWindow('Parameters')
                print("Parameter window closed")
        
        # 's': パラメータ保存
        elif key == ord('s'):
            save_params()
        
        # 'l': パラメータ読込
        elif key == ord('l'):
            if load_params() and param_window_visible:
                # トラックバーの位置を更新
                cv2.setTrackbarPos('YCrCb Min Y', 'Parameters', params['ycrcb_min_y'])
                cv2.setTrackbarPos('YCrCb Min Cr', 'Parameters', params['ycrcb_min_cr'])
                cv2.setTrackbarPos('YCrCb Min Cb', 'Parameters', params['ycrcb_min_cb'])
                cv2.setTrackbarPos('YCrCb Max Y', 'Parameters', params['ycrcb_max_y'])
                cv2.setTrackbarPos('YCrCb Max Cr', 'Parameters', params['ycrcb_max_cr'])
                cv2.setTrackbarPos('YCrCb Max Cb', 'Parameters', params['ycrcb_max_cb'])
                
                cv2.setTrackbarPos('HSV Min H', 'Parameters', params['hsv_min_h'])
                cv2.setTrackbarPos('HSV Min S', 'Parameters', params['hsv_min_s'])
                cv2.setTrackbarPos('HSV Min V', 'Parameters', params['hsv_min_v'])
                cv2.setTrackbarPos('HSV Max H', 'Parameters', params['hsv_max_h'])
                cv2.setTrackbarPos('HSV Max S', 'Parameters', params['hsv_max_s'])
                cv2.setTrackbarPos('HSV Max V', 'Parameters', params['hsv_max_v'])
                
                cv2.setTrackbarPos('Min Area (x100)', 'Parameters', params['min_area'] // 100)
                cv2.setTrackbarPos('Morph Close Iter', 'Parameters', params['morph_close'])
                cv2.setTrackbarPos('Morph Open Iter', 'Parameters', params['morph_open'])
        
        # 'd': デバッグモード
        elif key == ord('d'):
            debug_mode = not debug_mode
            print(f"Debug mode: {'ON' if debug_mode else 'OFF'}")
            if not debug_mode:
                for name in ['ycrcb', 'hsv', 'combined', 'filtered']:
                    try:
                        cv2.destroyWindow(f'Mask: {name}')
                    except:
                        pass
        
        # 'q': 終了
        elif key == ord('q'):
            break
    
    # リソースを解放
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()