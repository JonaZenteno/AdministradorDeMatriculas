# Versión 1.0.0 - Dominio Público

## About Dialog

Se ha agregado un footer sutil en la parte inferior derecha de la aplicación con el texto:

```
v1.0.0 - Dominio Público
```

Este texto es **interactivo** — al hacer clic sobre él, se abre un diálogo modal que muestra la Card del Desarrollador con la siguiente información:

- **Nombre**: Jona Zenteno
- **Rol**: Ingeniero en Informática
- **LinkedIn**: linkedin.com/in/jonathanzenteno/
- **Versión**: 1.0.0
- **Licencia**: Dominio Público

## Cards del Desarrollador

La imagen `card_dev.png` debe copiarse a la carpeta `assets/` de la aplicación. Si la imagen no se encuentra, el diálogo mostrará la información de texto con un fallback elegante.

### Estructura esperada:
```
ProyectoMatricula/
├── assets/
│   ├── logo.png
│   └── card_dev.png  ← Copiar la imagen aquí
├── modules/
├── main.py
└── ...
```

## Cambios realizados

- ✅ **Footer**: Se agregó un frame de footer con grid row 2
- ✅ **Label versión**: Texto sutil "v1.0.0 - Dominio Público" alineado a la derecha
- ✅ **Dialog**: Función `show_about_dev()` que abre una ventana modal
- ✅ **Tamaño ventana**: Aumentado de 700px a 750px de alto para acomodar el footer
- ✅ **Fallback**: Si la imagen no existe, muestra texto con información del desarrollador

## Cómo funciona

1. Al iniciar la aplicación, verás en la esquina inferior derecha: `v1.0.0 - Dominio Público`
2. Haz clic sobre ese texto
3. Se abre una ventana modal con la información del desarrollador
4. La ventana se cierra haciendo clic en "Cerrar"

---

Esta funcionalidad mantiene el diseño profesional y minimalista de la aplicación.
