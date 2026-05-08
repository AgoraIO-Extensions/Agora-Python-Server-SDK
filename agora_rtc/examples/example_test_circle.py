import matplotlib.pyplot as plt
import numpy as np

def draw_heart_matplotlib():
    # 创建图形
    plt.figure(figsize=(10, 10))
    plt.axis('off')
    
    # 创建心形数据
    t = np.linspace(0, 2*np.pi, 1000)
    x = 16 * np.sin(t)**3
    y = 13 * np.cos(t) - 5 * np.cos(2*t) - 2 * np.cos(3*t) - np.cos(4*t)
    
    # 绘制心形
    plt.plot(x, y, color='red', linewidth=2)
    plt.fill(x, y, color='red', alpha=0.5)
    
    # 添加文字
    plt.text(0, 0, 'header', fontsize=36, ha='center', va='center', color='white')
    plt.text(0, -5, 'some thing', fontsize=24, ha='center', va='center', color='white')
    
    # 设置背景
    plt.gca().set_facecolor('black')
    plt.gcf().set_facecolor('black')
    
    # 显示图形
    plt.show()

if __name__ == "__main__":
    draw_heart_matplotlib()
