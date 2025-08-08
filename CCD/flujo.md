```mermaid
graph TD
    A[Inicio] --> B[Inicialización de la ventana]
    B --> C[Cargar UI desde CCD.ui]
    C --> D[Configurar tamaño y posición]
    D --> E[Iniciar variables]
    E --> F[Configurar interfaz de usuario]
    F --> G[Configurar gráfico]
    G --> H[Configurar sliders]
    H --> I[Conectar señales y slots]
    I --> J[Mostrar gráfico]
    J --> K[Esperar eventos]
    K --> L[Interactuar con UI]
    L --> M[Actualizar sliders]
    L --> N[Seleccionar punto]
    L --> O[Calcular cinemática]
    L --> P[Actualizar ángulo]
    L --> Q[Actualizar precisión]
    L --> R[Actualizar velocidad]
    L --> S[Actualizar tipo de articulación]
    L --> T[Detener simulación]
    M --> U[Normalizar eslabones]
    U --> V[Actualizar gráfico]
    N --> W[Procesar clic en gráfico]
    W --> X[Actualizar punto objetivo]
    X --> V
    O --> Y[Simular cinemática inversa]
    Y --> Z[Actualizar trayectoria]
    Z --> V
    P --> AA[Actualizar ángulo de cambio]
    AA --> V
    Q --> AB[Actualizar precisión]
    AB --> V
    R --> AC[Actualizar velocidad]
    AC --> V
    S --> AD[Actualizar tipo de articulación]
    AD --> V
    T --> AE[Detener temporizador]
    AE --> V
    V --> AF[Fin]
