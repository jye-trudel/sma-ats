Web VPython 3.2

def read_data():
    in_file = read_local_file(scene.title_anchor)
    lines = in_file.text.split('\n')
    
    times = []
    prices = []
    
    for idx, line in enumerate(lines):
        if line.strip():  
            try:
                datetime_str, price_str = line.split(',')
                times.append(idx * 60)  
                prices.append(float(price_str))  
            except ValueError as e:
                print(f"Error parsing line: {line}. Error: {e}")
                pass  

    return times, prices

def calculate_sma(prices, window_size):
    sma = []
    for i in range(len(prices)):
        if i < window_size - 1:
            sma.append(None)  
        else:
            sma.append(sum(prices[i - window_size + 1:i + 1]) / window_size)
    return sma

def predict_next_price(prices, window_size):
    if len(prices) < window_size:
        return prices[-1]  

    
    total_diff = 0
    for i in range(1, window_size):
        total_diff += prices[-i] - prices[-i - 1]
    
    average_diff = total_diff / (window_size - 1)
    predicted_price = prices[-1] + average_diff
    
    return predicted_price

times, prices = read_data()
window_size = 5 
sma = calculate_sma(prices, window_size)

point = sphere(pos=vec(0, prices[0], 0), radius=2, color=color.white, make_trail=True)

x = box(pos=vec(point.pos.x + 70, point.pos.y - 40, 0), size=vec(140, 2, 5), axis=vec(0, 0, 0), color=color.white)
y = box(pos=vec(point.pos.x, point.pos.y, 0), size=vec(2, 80, 5), axis=vec(0, 0, 0), color=color.white)

price_label = box(pos=vec(point.pos.x + 1, point.pos.y, 5), size=vec(6, 2, 1), axis=vec(0, 0, 0), color=color.white)
price_text = text(text=str(prices[0]) + " ", pos=vec(price_label.pos.x - 20, price_label.pos.y - 1, 5), color=color.white, height=3)
p = point.pos.y + 50
current_price_text = text(text="USD$" + str(prices[0]), pos=vec(120, p, 0), color=color.white, height=5)
y_text = text(text="Price", pos=vec(y.pos.x - 5, y.pos.y + 45, 0), color=color.white, height=4)
x_text = text(text="Time", pos=vec(x.pos.x + 75, x.pos.y, 0), color=color.white, height=4)
scene.camera.pos = vec(point.pos.x + 70, point.pos.y, 0)
scene.range = 70

for i in range(len(prices)):
    rate(10)
    
    
    if point.pos.y > prices[0]:
        point.color = color.green
        point.trail_color = color.green
        price_label.color = color.green
        price_text.color = color.green
    elif point.pos.y < prices[0]:
        point.color = color.red
        point.trail_color = color.red
        price_label.color = color.red
        price_text.color = color.red
    
    
    if sma[i] is not None and prices[i] == sma[i]:
        point.color = color.yellow
        point.trail_color = color.yellow
        price_label.color = color.yellow
        price_text.color = color.yellow
    
    point.pos.y = prices[i]
    point.pos.x += 1
    price_label.pos.y = prices[i]
    price_text.visible = False
    price_text = text(text=str(prices[i]), pos=vec(price_label.pos.x - 20, price_label.pos.y - 1, 5), color=color.white, height=3)
    price_text.pos.y = prices[i] - 1
    current_price_text.visible = False
    current_price_text = text(text="USD$" + str(prices[i]), pos=vec(120, p, 0), color=color.white, height=5)
    
    
    if i >= window_size - 1:
        predicted_price = predict_next_price(prices[:i + 1], window_size)
        prices.append(predicted_price)


if len(prices) > len(times):
    for i in range(len(times), len(prices)):
        rate(10)
        if point.pos.x > x_text.pos.x:
            break
        point.color=color.yellow
        point.trail_color=color.yellow
        price_label.color = color.yellow
        price_text.color = color.yellow
        point.pos.y = prices[i]
        point.pos.x += 1
        price_label.pos.y = prices[i]
        price_text.visible = False
        price_text = text(text=str(prices[i]), pos=vec(price_label.pos.x - 20, price_label.pos.y - 1, 5), color=color.white, height=3)
        price_text.pos.y = prices[i] - 1
        current_price_text.visible = False
        current_price_text = text(text="USD$" + str(prices[i]), pos=vec(120, p, 0), color=color.white, height=5)
