# Gestor de Colección de Cartas y Barajas - GWENT
Un aplicativo web para gestionar una colección de cartas TCG (Gwent) y creación de mazos. Con el uso API REST para crear, listar, editar y eliminar (CRUD) cartas y mazos, validación reglas de construcción de mazos, ofreciendo vistas HTML con formularios para administrar cartas y barajas desde el navegador. Con el uso de bases de datos externas para almacenar y administrar los datos que registre el usuario junto con archivos multimedia.

<img width="1913" height="1034" alt="Interfaz" src="https://github.com/user-attachments/assets/65686f69-fa20-41fa-b7f5-b3ad16943dcd" />

## Organización de Carpetas

El proyecto sigue una estructura modular para separar la lógica de base de datos, los modelos de datos y la interfaz de usuario (Cliente-Servidor)


```
Web/
├── templates/           # Directorio de plantillas
│   ├── Dashboard.html   # Panel principal con filtros y lista de cartas/mazos.
│   ├── card.html        # Vista individual detallada de una carta.
│   ├── create_card.html # Formulario para el registro de nuevas cartas.
│   ├── edit_card.html   # Formulario para modificar cartas existentes.
│   ├── create_deck.html # Interfaz para crear un nuevo mazo.
│   └── deck_detail.html # Panel de gestión del mazo.
├── main.py              # Punto de entrada de FastAPI.
├── model.py             # Definición de modelos de base de datos (SQLAlchemy) y esquemas de datos (Pydantic).
├── repository.py        # Centralizador de operaciones CRUD genéricas en la base de datos.
├── database.py          # Configuración de la conexión a PostgreSQL (Neon) y Supabase Storage.
└── requirements.txt     # Listado de librerías y dependencias del proyecto.

```
## Modelos de Datos

<p align="center"> <img width="643" height="651" alt="Modelos" src="https://github.com/user-attachments/assets/cbc5dcf2-87cb-41f3-84d3-5abea3206b3d" /> </p>


*   **(Tabla `cards`)**: Almacena la información de cada carta.
    *   `id`: Identificador único (Primary Key).
    *   `name`: Nombre de la carta.
    *   `type`: Categoría (Unit, Hero, Leader, Special, Weather).
    *   `faction`: Facción a la que pertenece (o Neutral).
    *   `power`: Poder de ataque (0 para no unidades).
    *   `row`: Fila de combate (Melee, Range, Siege, Agile, None).
    *   `ability`: Efecto especial de la carta.
    *   `image_url`: Enlace a la imagen almacenada en Supabase.

*   **(Tabla `decks`)**: Define las barajas creadas.
    *   `id`: Identificador único (Primary Key).
    *   `name`: Nombre personalizado del mazo.
    *   `faction`: Facción asignada (determina qué cartas puede contener).
    *   `leader_id`: Referencia al ID de la carta líder.

*   **(Tabla `deck_cards`)**: Tabla intermedia para la relación Muchos a Muchos entre Mazos y Cartas.
    *   `deck_id`: ID del mazo.
    *   `card_id`: ID de la carta.
    *   `quantity`: Cantidad de copias de esa carta en el mazo.

### Esquemas de validación (Pydantic)

Se utilizan para asegurar que los datos recibidos a través de los endpoints de la API sean correctos:

*   **`Card`**: Valida los datos al crear o consultar cartas.
*   **`Deck`**: Estructura requerida para registrar un nuevo mazo.
*   **`DeckCard`**: Esquema para gestionar la adición de cartas a una baraja específica.

###  Relaciones Lógicas
*   **Relación 1:N**: Un **Mazo** tiene un **Líder** único (referenciado por `leader_id`).
*   **Relación N:M**: Un **Mazo** puede contener muchas **Cartas**, y una **Carta** puede estar presente en múltiples **Mazos** a través de la tabla `deck_cards`.

##  Mapa de Endpoints

<img width="1912" height="1043" alt="Docs" src="https://github.com/user-attachments/assets/22c5395a-05e4-4f67-bf7e-0d872909f156" />


### 🃏 Gestión de Cartas (JSON API)
*   `POST /cards`: Registra una nueva carta en el sistema.
*   `GET /cards`: Lista todas las cartas. Soporta filtros por `id`, `faction`, `type`, `power` y `row`.
*   `POST /cards/{card_id}/image`: Sube una imagen a Supabase Storage y la vincula a una carta.
*   `DELETE /cards/{card_id}`: Elimina una carta y limpia sus referencias en cualquier mazo.

### ⚔️ Gestión de Mazos (JSON API)
*   `POST /decks`: Crea una nueva baraja (requiere nombre y líder).
*   `DELETE /decks/{deck_id}`: Elimina un mazo completo.
*   `POST /decks/cards`: Añade una cantidad específica de copias de una carta a un mazo.
*   `GET /decks/{deck_id}/cards`: Obtiene el listado detallado de cartas dentro de un mazo.
*   `DELETE /decks/{deck_id}/cards/{card_id}`: Quita una carta específica de un mazo.
*   `GET /decks/{deck_id}/validate`: Ejecuta el motor de reglas de Gwent para verificar si el mazo es válido para jugar.

### 🌐 Interfaz Web (HTML)
*   `GET /`: **Dashboard principal**. Visualización de toda la colección y mazos creados.
*   `GET /cards_html/{card_id}`: Vista detallada de una carta con su ilustración.
*   `GET /create_card`: Formulario para registrar una nueva carta.
*   `GET /edit_card/{card_id}`: Formulario para modificar datos de una carta.
*   `GET /create_deck`: Formulario para la creación de barajas.
*   `GET /decks_html/{deck_id}`: **Gestor de Mazo**. Permite añadir/quitar cartas visualmente y ver el estado de validación en tiempo real.

### 🛠 Procesamiento de Formularios
*   `POST /cards_form`: Procesa el registro de cartas (incluyendo la subida de imagen).
*   `POST /cards_edit_form/{card_id}`: Procesa las actualizaciones de cartas.
*   `POST /decks_html/{deck_id}/add_card`: Añade cartas al mazo validando facción y límites de cartas especiales.
