from flask import Flask, render_template, request
from collections import Counter
import mushroom as m

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():
    result = None

    if request.method == 'POST':
        hand = []

        for i in range(1, 6):
            card = request.form.get(f'card{i}')

            hand.append(card)

        mushroom = request.form.get('mushroom') is not None

        #print("HAND:", hand)
        #print("BASE10:", m.base_sum(hand))
        #print("COMBOS:", m.validcombos(hand)) # for debugging

        hand = [card for card in hand if card != ""]

        if len(hand) != 5:
            result = "Please select exactly 5 cards."
        else:
            result = m.cow(hand, mushroom)

    return render_template('index.html', result=result)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)