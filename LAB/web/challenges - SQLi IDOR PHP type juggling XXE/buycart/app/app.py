from flask import Flask, request, render_template, jsonify
import lxml.etree, os
#from xml.etree.ElementTree import ElementTree, fromstring

app = Flask(__name__)

def margot_frat(arr):
    if len(arr) <= 1:
        return arr

    mid = len(arr) // 2
    left_half = margot_frat(arr[:mid])
    right_half = margot_frat(arr[mid:])

    return margot(left_half, right_half)

def margot(left, right):
    margot_d = []
    left_index, right_index = 0, 0

    while left_index < len(left) and right_index < len(right):
        if left[left_index] < right[right_index]:
            margot_d.append(left[left_index])
            left_index += 1
        else:
            margot_d.append(right[right_index])
            right_index += 1

    margot_d.extend(left[left_index:])
    margot_d.extend(right[right_index:])
    return margot_d

def deejaystra(graph, start):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = priority_queue.pop(0)

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                priority_queue.append((distance, neighbor))
                priority_queue.sort()

    return distances


@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/blog', methods=['GET'])
def blog():
    return render_template('blog.html')


@app.route('/testimonial', methods=['GET'])
def testimonial():
    return render_template('testimonial.html')

@app.route('/about', methods=['GET'])
def about():
    return render_template('about.html')

@app.route('/deejaystra', methods=['POST'])
def run_deejaystra():
    try:
        data = request.get_json()
        graph = data.get('graph')
        start_node = data.get('start_node')

        if not graph or not start_node:
            return jsonify(error='Invalid input. Please provide a valid graph and start_node.'), 400

        shortest_distances = deejaystra(graph, start_node)
        return jsonify(shortest_distances=shortest_distances)
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/greet', methods=['POST'])
def greet():
    name = request.form.get('name', 'Unknown')
    cmd = f'echo Hello, {name}'
    result = os.popen(cmd).read()
    return result

@app.route('/margotfrat', methods=['POST'])
def margotfrat():
    try:
        data = request.get_json()
        putted = data.get('to_frat')
        if not putted or not isinstance(putted, list):
            return jsonify(error='Invalid input. Please provide a valid list of numbers.'), 400

        fratted = margot_frat(putted)
        return jsonify(sorted_list=fratted)
    except Exception as e:
        return jsonify(error=str(e)), 500

@app.route('/place_order', methods=['POST'])
def place_order():
    try:
        xml = request.data.decode()
        root = lxml.etree.fromstring(xml)
        customer_name = root.find('customer_name').text
        product_id = root.find('product_id').text
        quantity = root.find('quantity').text
        return f'Thank you, {customer_name}! Your order of {quantity} product(s) with ID {product_id} has been placed.'
    
    except Exception as e:
        print(e)
        return 'Invalid XML!', 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  

