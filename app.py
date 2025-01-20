from flask import Flask, render_template, request, redirect, url_for, Response
from mysql import connector
from io import BytesIO

app = Flask(__name__)

db = connector.connect(
    host="qms5e.h.filess.io",
    database="izamiStore_soonjungle",
    user="izamiStore_soonjungle",
    password="11cb95020d41e7997b598c9546535104865d1971",
    port="3306"
)

if db.is_connected():
    print('Open connection successful')

@app.route('/gambar/<int:id>')
def gambar(id):
    cur = db.cursor()
    cur.execute('SELECT image FROM products WHERE id=%s', (id,))
    image_data = cur.fetchone()[0]
    cur.close()
    if image_data:
        return Response(image_data, mimetype='image/jpeg')
    return 'Image not found', 404

@app.route('/')
def halaman_awal():
    cur = db.cursor()
    cur.execute("SELECT * FROM products")
    hasil = cur.fetchall()
    cur.close()
    return render_template('index.html', hasil=hasil)

@app.route('/admin/')
def admin_ds():
    cur = db.cursor()
    cur.execute("SELECT * FROM products")
    hasil = cur.fetchall()
    cur.close()
    return render_template('admin.html', hasil=hasil)

@app.route('/tambah/')
def tambah_data():
    return render_template('tambah.html')

@app.route('/proses_tambah/', methods=['POST'])
def proses_tambah():
    id = request.form.get('id', '').strip()
    WhatsApp = request.form.get('WhatsApp', '').strip()
    image = request.form.get('image', '').strip()
    Product_name = request.form.get('Product_name', '').strip()
    Price = request.form.get('Price', '').strip()

    if not WhatsApp or not Product_name or not Price:
        return render_template('tambah.html', error="Semua field wajib diisi.")
    
    cur = db.cursor()
    cur.execute("SELECT * FROM products WHERE id = %s", (id,))
    existing_products = cur.fetchone()
    cur.close()

    if existing_products:
        return render_template('tambah.html', error="Nama sudah ada. Mohon gunakan nama yang berbeda.")

    cur = db.cursor()
    cur.execute(
        'INSERT INTO products (id, WhatsApp, Image, Product_name, Price) VALUES (%s, %s, %s, %s, %s)',
        (id, WhatsApp, image, Product_name, Price)
    )
    db.commit()
    cur.close()
    return redirect(url_for('admin_ds'))

@app.route('/ubah/<Product_name>', methods=['GET'])
def ubah_data(Product_name):
    cur = db.cursor()
    cur.execute('SELECT * FROM products WHERE Product_name=%s', (Product_name,))
    hasil = cur.fetchone()
    cur.close()
    if hasil:
        return render_template('ubah.html', hasil=[hasil])
    else:
        return redirect(url_for('admin_ds'))

@app.route('/proses_ubah/', methods=['POST'])
def proses_ubah():
    product_awal = request.form['product_awal']
    id = request.form.get('id', '').strip()
    WhatsApp = request.form.get('WhatsApp', '').strip()
    image = request.form.get('image', '').strip()
    Product_name = request.form.get('Product_name', '').strip()
    Price = request.form.get('Price', '').strip()

    cur = db.cursor()
    sql = "UPDATE products SET id=%s, WhatsApp=%s, image=%s, Product_name=%s, Price=%s WHERE Product_name=%s"
    values = (id, WhatsApp, image, Product_name, Price, product_awal)
    cur.execute(sql, values)
    db.commit()
    cur.close()
    return redirect(url_for('admin_ds'))

@app.route('/hapus/<Product_name>', methods=['GET'])
def hapus_data(Product_name):
    cur = db.cursor()
    cur.execute('DELETE FROM products WHERE Product_name=%s', (Product_name,))
    db.commit()
    cur.close()
    return redirect(url_for('admin_ds'))

if __name__ == '__main__':
    app.run(debug=True)
