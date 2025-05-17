def game_start():
    print("你坐在寧靜的草地上，陽光灑在身上。")
    print("你可以選擇往前後左右移動。")
    player_action()

def player_action():
    has_map = False # 追蹤主角是否擁有地圖
    has_coins_right = False # 追蹤是否在右邊撿過金幣
    has_sword = False # 追蹤主角是否擁有寶劍

    while True:
        direction = input("你想往哪個方向走？(前/後/左/右/離開/m): ").lower()
        if direction == "前":
            print("你向前走去，看到了一家小商店。")
            if has_coins_right and not has_sword:
                choice = input("店主向你展示一把閃亮的寶劍。你想要購買嗎？(是/否): ").lower()
                if choice == "是":
                    print("你用金幣買下了寶劍。")
                    has_sword = True
                else:
                    print("你謝絕了店主的好意，繼續向前走去。")
            elif has_sword:
                print("你已經擁有一把寶劍了，繼續向前走去。")
            else:
                print("你身上沒有足夠的金幣，只能先看看，然後繼續向前走去。")
            # 在這裡可以加入更多商店互動或往前移動後的其他事件
        elif direction == "後":
            print("你往後看去，只見一片茂密的草地，沒有其他特別的東西。")
        elif direction == "左":
            print("你往左走去，發現了一個黑漆漆的山洞。")
            if not has_map:
                has_map = explore_cave(has_sword) # 呼叫探索山洞的函數並傳遞是否擁有寶劍
                if has_map:
                    print("你獲得了一張粗略的地圖。")
            else:
                print("你已經擁有地圖，可以更清楚地知道山洞的位置。")
                choice = input("你想要再次進入山洞探索嗎？(是/否): ").lower()
                if choice == "是":
                    explore_cave(has_sword, already_has_map=True)
                else:
                    print("你決定今天不再深入探索山洞。")
        elif direction == "右":
            if not has_coins_right:
                print("你向右走去，發現了一袋金幣！")
                has_coins_right = True
            else:
                print("你向右邊看去，這裡沒有其他東西了。")
        elif direction == "離開":
            print("你結束了探索。")
            break
        elif direction == "m":
            if has_map:
                print("\n--- 地圖 ---")
                print("前方: 一家小商店")
                print("後方: 一片茂密的草地")
                print("左方: 一個黑漆漆的山洞")
                print("右方: 一些散落的金幣 (你可能已經撿過了)")
                print("-------------\n")
            else:
                print("你還沒有地圖，不知道周圍的環境。")
        else:
            print("無效的指令，請輸入 前、後、左、右、離開 或 m。")

def explore_cave(has_sword, already_has_map=False):
    print("\n你小心翼翼地走進山洞，裡面一片昏暗，只能聽到水滴聲。")
    if not already_has_map:
        print("在山洞深處，你發現了一個小箱子。")
        input("你打開箱子... (按下 Enter)")
        print("裡面有一張捲起來的羊皮紙，看起來像是一張地圖。")
        if has_sword:
            print("你握緊了手中的寶劍，感覺更有信心面對潛在的危險。")
            choice = input("你想要繼續深入探索山洞嗎？(是/否): ").lower()
            if choice == "是":
                print("\n你鼓起勇氣，繼續往山洞深處走去...")
                print("突然，一隻可怕的怪獸出現在你面前！")
                print("你揮舞手中的寶劍，與怪獸展開激烈的戰鬥！")
                print("你成功地擊敗了怪獸！")
                print("\n恭喜你！你用寶劍擊敗了怪獸，完成了你的冒險！")
                input("按下 Enter 鍵結束遊戲。")
                quit() # 直接結束程式
            else:
                print("你決定先拿到地圖就好，原路返回洞口。")
        else:
            print("突然感覺山洞深處傳來一股不祥的氣息。")
            print("你決定不再冒險，原路返回洞口。")
        return True # 返回 True 表示主角拿到了地圖
    else:
        if has_sword:
            print("你手持寶劍，再次進入山洞。")
            choice = input("你想要繼續深入探索山洞嗎？(是/否): ").lower()
            if choice == "是":
                print("\n你鼓起勇氣，繼續往山洞深處走去...")
                print("突然，一隻可怕的怪獸出現在你面前！")
                print("你揮舞手中的寶劍，與怪獸展開激烈的戰鬥！")
                print("你成功地擊敗了怪獸！")
                print("\n恭喜你！你用寶劍擊敗了怪獸，完成了你的冒險！")
                input("按下 Enter 鍵結束遊戲。")
                quit() # 直接結束程式
            else:
                print("你決定這次先探索到這裡。")
        else:
            print("你沒有寶劍，感覺山洞深處可能會有危險，決定在洞口附近探索一下。")
            print("（在這裡可以加入在洞口附近探索的事件）")
        return True # 即使已經有地圖，也返回 True，表示這次進入了山洞

if __name__ == "__main__":
    game_start()