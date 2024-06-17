from flask import Flask, jsonify, make_response, render_template, request, redirect, session, url_for
from BD import BD
from werkzeug.security import check_password_hash, generate_password_hash

bd = BD()
app = Flask(__name__)
app.secret_key = "secret_key"


@app.route("/")
def principal():
    tipos = bd.verTiposAtaxia()
    return render_template("principal.html", tipos=tipos)

@app.route("/index")
def index():
    publis = bd.verPublicaciones()
    usuario = session.get("usuario", None)
    return render_template("index.html", usuario=usuario, publis=publis)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        usuario = bd.login(request.form["usuario"])
        clave = request.form["clave"]
        # if usuario is None:
        if usuario==0:
            return render_template("login.html", error="El usuario introducido no existe")
        elif (check_password_hash(usuario[2], clave)):
        # elif usuario[2] == clave:
            session["usuario"] = usuario
            if request.form.get("recordar"):
                # Si la casilla de verificación de "recordar" está marcada, establece una cookie
                respuesta = make_response(redirect("/"))
                usuario_nombre = str(usuario[1])  # Asegurarse de que el nombre de usuario sea una cadena
                respuesta.set_cookie("usuario", usuario_nombre, max_age=604800)  # La cookie expira en una semana (604800 segundos)
                return respuesta
            return redirect("/index")
        else:
            return render_template("login.html", error="Contraseña incorrecta")
    else:
        return render_template("login.html")

    
@app.route("/registro", methods=["GET", "POST"])
def registro():
    roles = bd.roles()
    if request.method == "POST":
        usuario = request.form["usuario"]
        clave = request.form["clave"]
        confirmar_clave = request.form["confirmar_clave"]
        rol = request.form["rol"]

        # Comprobar si la clave y la confirmación de la clave coinciden
        
        if clave != confirmar_clave:
            return render_template("registro.html", error="Las contraseñas no coinciden", roles=roles)

        comprobacion = bd.login(usuario)
        if comprobacion==0:
            pw=generate_password_hash(clave)
            bd.registrar(usuario,pw,rol)
            return redirect("/login")
        else:
            return render_template("registro.html", error="El usuario introducido ya existe", roles=roles)

    else:
    
        return render_template("registro.html", roles=roles)


@app.route('/logout')
def logout():
    session.pop('usuario', None)
    return redirect(url_for("index"))


@app.route("/publicar", methods=["GET", "POST"])
def publicar():
    if "usuario" not in session:
        return redirect(url_for("login"))
    
    if request.method == "POST":
        idUsuario = session["usuario"][0]  # coge el ID del usuario que ha iniciado sesion
        nombreAtaxia=request.form["ta"]
        idTipoAtaxia=bd.obtenerIdTipotaxia(nombreAtaxia)
        descripcion=request.form["descripcion"]
        bd.publicar(idUsuario,idTipoAtaxia,descripcion)
        return render_template("publicar.html",mensaje="Publicación hecha correctamente")
    else:
        tiposAtaxia=bd.tipoAtaxia()
        return render_template("publicar.html", tiposAtaxia=tiposAtaxia)
        
@app.route("/like/<int:idPublicacion>", methods=["POST"])
def like(idPublicacion):
    if "usuario" not in session:
        return jsonify({"success": False, "error": "Debe iniciar sesión para dar me gusta"})

    idUsuario = session["usuario"][0]
    if bd.usuarioHaDadoLike(idUsuario, idPublicacion):
        bd.quitarLike(idUsuario, idPublicacion)
        return jsonify({"success": True, "likes": bd.likes(idPublicacion), "alreadyLiked": False})
    else:
        bd.meGusta(idUsuario, idPublicacion)
        return jsonify({"success": True, "likes": bd.likes(idPublicacion), "alreadyLiked": True})

@app.route('/eliminar/<int:idPublicacion>', methods=['POST'])
def eliminar(idPublicacion):
    bd.eliminar(idPublicacion)
    jsonify('Publicación eliminada correctamente.', 'success')
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(error):
    return render_template("error.html", error="Lo sentimos. Página no encontrada...")

if __name__ == "__main__":
    app.run(debug=True)
    
