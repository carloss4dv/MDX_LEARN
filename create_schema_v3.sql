-- SQLite Schema based on schema_final_v3.dbml
-- Version: Final v3

PRAGMA foreign_keys = ON;

-- --- Conformed Dimensions ---

CREATE TABLE DimTiempo (
    TiempoKey INTEGER PRIMARY KEY, -- Surrogate Key
    Fecha TEXT UNIQUE, -- Specific date, ISO 8601 format YYYY-MM-DD
    Anio INTEGER NOT NULL,
    Mes INTEGER NOT NULL,
    Dia INTEGER,
    Trimestre INTEGER,
    Semestre INTEGER,
    DiaSemana TEXT,
    CursoAcademico TEXT NOT NULL, -- e.g., 2023/2024
    FechaActualizacion TEXT -- Last data load date, ISO 8601 format
);

CREATE TABLE DimCentro (
    CentroKey INTEGER PRIMARY KEY, -- Surrogate Key
    CodigoCentro TEXT UNIQUE NOT NULL,
    NombreCentro TEXT,
    TipoCentro TEXT, -- Facultad, Escuela, Adscrito, IUI, etc.
    Campus TEXT,
    Localidad TEXT
);

CREATE TABLE DimDepartamento (
    DepartamentoKey INTEGER PRIMARY KEY, -- Surrogate Key
    CodigoDepartamento TEXT UNIQUE NOT NULL,
    NombreDepartamento TEXT,
    CentroAdscripcionKey INTEGER, -- Primary center affiliation
    FOREIGN KEY (CentroAdscripcionKey) REFERENCES DimCentro(CentroKey)
);

CREATE TABLE DimAreaConocimiento (
    AreaConocimientoKey INTEGER PRIMARY KEY,
    CodigoArea TEXT UNIQUE NOT NULL,
    NombreArea TEXT,
    MacroArea TEXT -- Artes y Humanidades, Ciencias, CC Sociales y Jurídicas, CC Salud, Ingeniería y Arq.
);

CREATE TABLE DimPlanEstudio (
    PlanEstudioKey INTEGER PRIMARY KEY, -- Surrogate Key
    CodigoPlan TEXT UNIQUE NOT NULL,
    NombrePlan TEXT,
    TipoEstudio TEXT NOT NULL, -- Grado, Master, Doctorado, Licenciatura, Diplomatura, Titulo Propio, Movilidad
    EstudioCodigo TEXT, -- Code for the broader Study (grouping Plans)
    EstudioNombre TEXT, -- Name for the broader Study
    CentroKey INTEGER NOT NULL, -- Center offering the plan
    RamaConocimiento TEXT, -- Arts & Humanities, Sciences, etc.
    CreditosTotales REAL,
    GradoExperimentalidad TEXT, -- From Matricula (since 2015/16)
    Interuniversitario INTEGER, -- 0/1
    CoordinaUnizar INTEGER, -- 0/1
    MasterHabilitante INTEGER, -- 0/1
    MultipleTitulacion INTEGER, -- 0/1
    DuracionCursos INTEGER, -- For Titulos Propios
    FechaInicio TEXT, -- ISO 8601 format
    FechaExtincion TEXT, -- ISO 8601 format
    FOREIGN KEY (CentroKey) REFERENCES DimCentro(CentroKey)
);

CREATE TABLE DimAsignatura (
    AsignaturaKey INTEGER PRIMARY KEY, -- Surrogate Key
    CodigoAsignatura TEXT UNIQUE NOT NULL,
    NombreAsignatura TEXT,
    ClaseAsignatura TEXT, -- Formación básica, Obligatoria, Optativa, TFG, TFM, Prácticas, Especial, etc.
    Creditos REAL,
    DepartamentoEncargadoKey INTEGER, -- Primary dept responsible
    DocenciaExterna INTEGER, -- 0/1
    OrigenVinculo INTEGER, -- 0/1 From DocenciaPDI
    TipoTratamientoDocencia TEXT, -- Normal, Prácticas, TFG/TFM, Departamental, Sin Docencia. From DocenciaPDI
    FOREIGN KEY (DepartamentoEncargadoKey) REFERENCES DimDepartamento(DepartamentoKey)
);

CREATE TABLE BridgeAsignaturaPlan (
    AsignaturaKey INTEGER NOT NULL,
    PlanEstudioKey INTEGER NOT NULL,
    PRIMARY KEY (AsignaturaKey, PlanEstudioKey),
    FOREIGN KEY (AsignaturaKey) REFERENCES DimAsignatura(AsignaturaKey),
    FOREIGN KEY (PlanEstudioKey) REFERENCES DimPlanEstudio(PlanEstudioKey)
);

CREATE TABLE DimPersona (
    PersonaKey INTEGER PRIMARY KEY, -- Surrogate Key
    IdentificadorPersona TEXT UNIQUE, -- DNI/NIE/ID - Use appropriate hashing/masking for privacy
    NombreCompleto TEXT,
    Sexo TEXT,
    FechaNacimiento TEXT, -- ISO 8601 format
    RangoEdad TEXT, -- Calculated at specific time points
    PaisNacionalidad TEXT,
    ResidenciaPais TEXT,
    ResidenciaCCAA TEXT,
    ResidenciaProvincia TEXT,
    ResidenciaPoblacion TEXT,
    PaisNacimiento TEXT,
    PoblacionNacimiento TEXT,
    NivelTitulacion TEXT, -- Highest achieved? From PTGAS, RRHHidi
    UniversidadOrigen TEXT, -- From Admision
    EsDoctor INTEGER, -- 0/1 From PDI, DocenciaPDI, Grupos, RRHHidi
    EsEstudiante INTEGER, -- 0/1
    EsPDI INTEGER, -- 0/1
    EsPTGAS INTEGER, -- 0/1
    EsSolicitanteAdmision INTEGER, -- 0/1
    EsInvestigador INTEGER, -- 0/1
    EsAutor INTEGER, -- 0/1
    TieneCargo INTEGER, -- 0/1
    EsBecario INTEGER -- 0/1
);

CREATE TABLE DimPuestoTrabajo (
    PuestoKey INTEGER PRIMARY KEY,
    CodigoPuesto TEXT UNIQUE,
    NombrePuesto TEXT NOT NULL,
    TipoPuesto TEXT, -- PDI/PAS
    CategoriaPuesto TEXT,
    NivelComplemento TEXT,
    GrupoPuesto TEXT,
    DedicacionPuesto TEXT, -- Tiempo completo, parcial, conjunta, etc.
    RegimenJuridico TEXT, -- Funcionario, Laboral, Atípico
    EsInvestigacion INTEGER, -- 0/1 From Puesto, RRHHidi
    VinculadoSanitarias INTEGER, -- 0/1
    CentroAdscripcionKey INTEGER,
    DepartamentoAdscripcionKey INTEGER,
    UnidadAdscripcion TEXT,
    EspecialidadRPT TEXT, -- From PTGAS
    FOREIGN KEY (CentroAdscripcionKey) REFERENCES DimCentro(CentroKey),
    FOREIGN KEY (DepartamentoAdscripcionKey) REFERENCES DimDepartamento(DepartamentoKey)
);

CREATE TABLE DimAtributosPDI (
    AtributosPDIKey INTEGER PRIMARY KEY,
    PersonaKey INTEGER UNIQUE NOT NULL,
    CategoriaCuerpoEscala TEXT,
    AreaConocimientoKey INTEGER,
    DepartamentoAdscripcionKey INTEGER,
    CentroAdscripcionKey INTEGER,
    TieneCompatibilidad INTEGER, -- 0/1
    EsAsociadoSanitario INTEGER, -- 0/1
    CargaDocenteSemanalHoras REAL,
    Dedicacion TEXT, -- Tiempo completo, parcial, conjunta, etc. From DocenciaPDI
    EsPermanente INTEGER, -- 0/1 Funcionario o Indefinido. From DocenciaPDI
    DocenciaQuinquenios INTEGER,
    GestionTrienios INTEGER, -- From DocenciaPDI, PTGAS
    InvestigacionSexeniosEstatales INTEGER, -- From DocenciaPDI, Grupos, RRHHidi
    SexeniosPosibles INTEGER, -- From DocenciaPDI, RRHHidi
    CategoriaInvestigador TEXT, -- From RRHHidi
    ModalidadPersonal TEXT, -- Carrera, Interino, Temporal, etc. From RRHHidi
    TesisDirigidas REAL, -- Count/Fraction. From RRHHidi
    TesisDirigidasInternacional REAL, -- Count/Fraction. From RRHHidi
    ParticipaProyecto INTEGER, -- 0/1 From RRHHidi
    ProgramaPresupuestarioPuesto TEXT, -- From RRHHidi
    EsPuestoInvestigacion INTEGER, -- 0/1 From RRHHidi, Puesto
    FOREIGN KEY (PersonaKey) REFERENCES DimPersona(PersonaKey),
    FOREIGN KEY (AreaConocimientoKey) REFERENCES DimAreaConocimiento(AreaConocimientoKey),
    FOREIGN KEY (DepartamentoAdscripcionKey) REFERENCES DimDepartamento(DepartamentoKey),
    FOREIGN KEY (CentroAdscripcionKey) REFERENCES DimCentro(CentroKey)
);

CREATE TABLE DimAtributosPTGAS (
    AtributosPTGASKey INTEGER PRIMARY KEY,
    PersonaKey INTEGER UNIQUE NOT NULL,
    CategoriaCuerpoEscala TEXT,
    Dedicacion TEXT, -- Tiempo completo/parcial
    GradoComplemento TEXT,
    GrupoLaboral TEXT, -- A1, A2, C1, etc.
    RegimenJuridico TEXT, -- Funcionario/Laboral
    SituacionAdministrativa TEXT, -- Servicio activo, Excedencia, etc.
    TipoPersonalContrato TEXT, -- Carrera, Interino, Indefinido, etc.
    TieneCompatibilidad INTEGER, -- 0/1
    GestionTrienios INTEGER,
    PuestoTrabajoKey INTEGER, -- Current or primary puesto
    TieneReduccionSindical INTEGER, -- 0/1
    SindicatoNombre TEXT,
    ReduccionSindicalHorasPorc TEXT,
    FOREIGN KEY (PersonaKey) REFERENCES DimPersona(PersonaKey),
    FOREIGN KEY (PuestoTrabajoKey) REFERENCES DimPuestoTrabajo(PuestoKey)
);

CREATE TABLE DimAtributosAlumno (
    AtributosAlumnoKey INTEGER PRIMARY KEY,
    PersonaKey INTEGER UNIQUE NOT NULL,
    EstudioPrevioAcceso TEXT, -- PAU, FP, Titulado, >25, etc.
    NuevoIngreso INTEGER, -- 0/1 First time in plan/university?
    RangoNotaAdmision TEXT,
    ModalidadMatricula TEXT, -- Tiempo completo/parcial
    CursoMasAltoMatriculado INTEGER,
    TrasladoContinuacionEstudio INTEGER, -- 0/1
    CreditosSuperadosPrevios TEXT, -- Range. From EstudiantesOUT, SolicitudesMovOUT
    CursosMatriculadosPrevios INTEGER, -- From EstudiantesOUT, SolicitudesMovOUT
    FOREIGN KEY (PersonaKey) REFERENCES DimPersona(PersonaKey)
);

CREATE TABLE DimProgramaMovilidad (
    ProgramaMovilidadKey INTEGER PRIMARY KEY, -- Surrogate Key
    CodigoPrograma TEXT UNIQUE,
    NombrePrograma TEXT, -- Erasmus, SICUE, America Latina, etc.
    TipoMovilidad TEXT, -- Entrada, Salida
    Ambito TEXT, -- Nacional, Internacional
    Colectivo TEXT, -- Alumnos, Docentes
    ProgramaInternacional INTEGER, -- 0/1 From EstudiantesIN/OUT
    TipoProgramaMovilidad TEXT -- Erasmus, SICUE, Otras UE, Otras fuera UE, etc. From EstudiantesIN/OUT
);

CREATE TABLE DimUniversidad (
    UniversidadKey INTEGER PRIMARY KEY,
    NombreUniversidad TEXT UNIQUE NOT NULL,
    PaisUniversidad TEXT,
    EsUNITA INTEGER -- 0/1 From Acuerdos, EstudiantesIN/OUT
);

CREATE TABLE DimAcuerdoBilateral (
    AcuerdoBilateralKey INTEGER PRIMARY KEY,
    ProgramaMovilidadKey INTEGER,
    UniversidadAcuerdoKey INTEGER,
    CentroResponsableUnizarKey INTEGER, -- 021 for General Scope
    CursoAcademicoVigencia TEXT NOT NULL,
    NivelEstudiosAcuerdo TEXT, -- Undergraduate, Postgraduate, etc.
    AreaEstudiosAcuerdo TEXT, -- From EstudiantesOUT, SolicitudesMovOUT
    IdiomaPrincipal TEXT,
    NivelIdiomaPrincipal TEXT,
    IdiomaSecundario TEXT,
    NivelIdiomaSecundario TEXT,
    MesesOfertadosPlaza INTEGER,
    FOREIGN KEY (ProgramaMovilidadKey) REFERENCES DimProgramaMovilidad(ProgramaMovilidadKey),
    FOREIGN KEY (UniversidadAcuerdoKey) REFERENCES DimUniversidad(UniversidadKey),
    FOREIGN KEY (CentroResponsableUnizarKey) REFERENCES DimCentro(CentroKey)
);

CREATE TABLE DimSolicitudAdmision (
    SolicitudAdmisionKey INTEGER PRIMARY KEY,
    PersonaKey INTEGER NOT NULL,
    PlanEstudioSolicitadoKey INTEGER NOT NULL,
    CursoAcademicoSolicitud TEXT NOT NULL,
    Convocatoria TEXT, -- Ordinaria/Extraordinaria
    TipoAcceso TEXT, -- Preinscripcion/MatriculaDirecta/AccesoCiclos
    CupoAdjudicacion TEXT, -- General, Reserva Discap, Titulados, >25, etc.
    EstudioPrevio TEXT, -- PAU, FP, Titulado, etc.
    OrdenPreferencia INTEGER, -- 1-10
    RangoCalificacionAdmision TEXT, -- 5-6, ..., 13-14
    EstadoSolicitud TEXT, -- Admitida, ListaEspera, Desactivada, etc.
    TipoProcedimientoReclamacion TEXT, -- Normal/Recurso
    PrelacionConvoNotaCorte TEXT, -- J/S, Obsolete after 2017/18
    FOREIGN KEY (PersonaKey) REFERENCES DimPersona(PersonaKey),
    FOREIGN KEY (PlanEstudioSolicitadoKey) REFERENCES DimPlanEstudio(PlanEstudioKey)
);

CREATE TABLE DimCargo (
    CargoKey INTEGER PRIMARY KEY,
    NombreCargo TEXT UNIQUE NOT NULL,
    TipoCargo TEXT, -- Vicerrector, Decano, Director Dept, etc.
    ImporteTeoricoComplemento REAL,
    ReduccionHorasPorcentaje TEXT,
    Remunerado INTEGER -- 0/1
);

CREATE TABLE DimTipoDocencia (
    TipoDocenciaKey INTEGER PRIMARY KEY,
    NombreTipoDocencia TEXT UNIQUE NOT NULL -- Clases magistrales, Resolución problemas, Prácticas Lab, etc.
);

CREATE TABLE DimResponsabilidadDocente (
    ResponsabilidadKey INTEGER PRIMARY KEY,
    NombreResponsabilidad TEXT UNIQUE NOT NULL -- Coordinar docencia, Impartir docencia, Dirigir
);

CREATE TABLE DimGrupoInvestigacion (
    GrupoInvKey INTEGER PRIMARY KEY,
    CodigoGrupo TEXT UNIQUE,
    NombreGrupo TEXT NOT NULL,
    TipoGrupo TEXT, -- Emergente, Consolidado, C.I.A., Excelente
    GestionadoPorUnizar INTEGER, -- 0/1
    InvestigadorPrincipalPersonaKey INTEGER,
    CentroIPKey INTEGER,
    DepartamentoIPKey INTEGER,
    InstitutoIPKey INTEGER, -- Assuming IUI are in DimCentro
    MacroareaIP TEXT,
    AreaIPKey INTEGER,
    FOREIGN KEY (InvestigadorPrincipalPersonaKey) REFERENCES DimPersona(PersonaKey),
    FOREIGN KEY (CentroIPKey) REFERENCES DimCentro(CentroKey),
    FOREIGN KEY (DepartamentoIPKey) REFERENCES DimDepartamento(DepartamentoKey),
    FOREIGN KEY (InstitutoIPKey) REFERENCES DimCentro(CentroKey),
    FOREIGN KEY (AreaIPKey) REFERENCES DimAreaConocimiento(AreaConocimientoKey)
);

CREATE TABLE BridgeInvestigadorGrupo (
    InvestigadorPersonaKey INTEGER NOT NULL,
    GrupoInvKey INTEGER NOT NULL,
    TipoMiembroGrupo TEXT, -- Investigador Principal, Colaborador, Becario, Externo
    FechaInicio TEXT, -- ISO 8601 format
    FechaFin TEXT, -- ISO 8601 format
    PRIMARY KEY (InvestigadorPersonaKey, GrupoInvKey, FechaInicio), -- For SCD Type 2 on membership
    FOREIGN KEY (InvestigadorPersonaKey) REFERENCES DimPersona(PersonaKey),
    FOREIGN KEY (GrupoInvKey) REFERENCES DimGrupoInvestigacion(GrupoInvKey)
);

CREATE TABLE DimRevista (
    RevistaKey INTEGER PRIMARY KEY,
    NombreRevista TEXT NOT NULL,
    ISSN TEXT UNIQUE
);

CREATE TABLE DimMateriaJCR (
    MateriaKey INTEGER PRIMARY KEY,
    NombreMateria TEXT UNIQUE NOT NULL
);

CREATE TABLE DimEstudioPropio (
    EstudioPropioKey INTEGER PRIMARY KEY,
    CodigoEstudioPropio TEXT UNIQUE,
    NombreEstudioPropio TEXT NOT NULL,
    TipoEstudioPropio TEXT, -- Máster Propio, Experto, Diploma Especialización, etc.
    RamaConocimiento TEXT,
    Modalidad TEXT, -- Presencial, Semipresencial, Online
    DuracionCursos INTEGER,
    Edicion INTEGER,
    OrganoGestionKey INTEGER,
    OrganoProponenteKey INTEGER,
    FOREIGN KEY (OrganoGestionKey) REFERENCES DimCentro(CentroKey),
    FOREIGN KEY (OrganoProponenteKey) REFERENCES DimCentro(CentroKey)
);

CREATE TABLE DimTipoEntidad (
    TipoEntidadKey INTEGER PRIMARY KEY,
    NombreTipoEntidad TEXT UNIQUE NOT NULL -- Empresa, Universidad, Unidad de Investigación, etc.
);

CREATE TABLE DimPublicacion (
    PublicacionKey INTEGER PRIMARY KEY,
    TipoPublicacion TEXT NOT NULL, -- Articulo, Libro, Capitulo
    Titulo TEXT,
    DOI TEXT UNIQUE,
    AnioPublicacion INTEGER,
    Idioma TEXT,
    EsArticuloAbierto INTEGER, -- 0/1 For Articulo
    TipoArticulo TEXT, -- Científico, Revisión, Editorial, etc. For Articulo
    RevistaKey INTEGER, -- For Articulo
    ISBN TEXT, -- For Libro/Capitulo
    Editorial TEXT, -- For Libro/Capitulo
    FOREIGN KEY (RevistaKey) REFERENCES DimRevista(RevistaKey)
);

CREATE TABLE BridgeAutorPublicacion (
    AutorPersonaKey INTEGER NOT NULL,
    PublicacionKey INTEGER NOT NULL,
    OrdenAutor INTEGER,
    EsCorrespondencia INTEGER, -- 0/1
    PRIMARY KEY (AutorPersonaKey, PublicacionKey),
    FOREIGN KEY (AutorPersonaKey) REFERENCES DimPersona(PersonaKey),
    FOREIGN KEY (PublicacionKey) REFERENCES DimPublicacion(PublicacionKey)
);

CREATE TABLE DimCongreso (
    CongresoKey INTEGER PRIMARY KEY,
    NombreCongreso TEXT NOT NULL,
    AnioCelebracion INTEGER,
    PaisCongreso TEXT,
    AmbitoGeograficoCongreso TEXT, -- Autonómico, Nacional, UE, Internacional no UE
    CategoriaCongreso TEXT -- A+, A, B, C, No clasificado
);

CREATE TABLE DimTipoActividadCongreso (
    TipoActividadKey INTEGER PRIMARY KEY,
    NombreTipoActividad TEXT UNIQUE NOT NULL -- Ponencia invitada, Ponencia, Póster, Comité Organizador, Comité Científico, Otros
);

CREATE TABLE BridgeAutorActividadCongreso (
    AutorPersonaKey INTEGER NOT NULL,
    CongresoKey INTEGER NOT NULL,
    TipoActividadKey INTEGER NOT NULL,
    TituloContribucion TEXT,
    PRIMARY KEY (AutorPersonaKey, CongresoKey, TipoActividadKey, TituloContribucion), -- Added Titulo to PK for uniqueness
    FOREIGN KEY (AutorPersonaKey) REFERENCES DimPersona(PersonaKey),
    FOREIGN KEY (CongresoKey) REFERENCES DimCongreso(CongresoKey),
    FOREIGN KEY (TipoActividadKey) REFERENCES DimTipoActividadCongreso(TipoActividadKey)
);

CREATE TABLE DimConvocatoriaProyecto (
    ConvocatoriaKey INTEGER PRIMARY KEY,
    CodigoConvocatoria TEXT UNIQUE,
    NombreConvocatoria TEXT,
    AnioConvocatoria INTEGER NOT NULL,
    Programa TEXT,
    Subprograma TEXT,
    LineaActuacion TEXT,
    TipoConvocatoria TEXT, -- Grupos, Proyectos I+D+I, Movilidades, RRHH, etc.
    TipoOportunidad TEXT, -- Contrato, Convenio, Convocatoria
    AmbitoTerritorial TEXT, -- Local, Autonómico, Nacional, Europeo, Internacional
    OficinaGestora TEXT, -- OPE, OTRI, SGI, Externos
    FechaResolucion TEXT -- ISO 8601 format
);

CREATE TABLE DimProyecto (
    ProyectoKey INTEGER PRIMARY KEY,
    CodigoProyecto TEXT UNIQUE NOT NULL,
    TituloProyecto TEXT,
    ConvocatoriaKey INTEGER,
    InvestigadorPrincipalPersonaKey INTEGER,
    FechaInicio TEXT, -- ISO 8601 format
    FechaFin TEXT, -- ISO 8601 format
    FOREIGN KEY (ConvocatoriaKey) REFERENCES DimConvocatoriaProyecto(ConvocatoriaKey),
    FOREIGN KEY (InvestigadorPrincipalPersonaKey) REFERENCES DimPersona(PersonaKey)
);

CREATE TABLE BridgeInvestigadorProyecto (
    InvestigadorPersonaKey INTEGER NOT NULL,
    ProyectoKey INTEGER NOT NULL,
    Rol TEXT, -- IP, Miembro Equipo, Colaborador
    PRIMARY KEY (InvestigadorPersonaKey, ProyectoKey),
    FOREIGN KEY (InvestigadorPersonaKey) REFERENCES DimPersona(PersonaKey),
    FOREIGN KEY (ProyectoKey) REFERENCES DimProyecto(ProyectoKey)
);

CREATE TABLE DimSolicitudProyecto (
    SolicitudProyKey INTEGER PRIMARY KEY,
    ConvocatoriaKey INTEGER NOT NULL,
    SolicitantePersonaKey INTEGER NOT NULL,
    ProyectoKey INTEGER, -- Link to project if granted
    FechaSolicitud TEXT, -- ISO 8601 format
    EstadoSolicitud TEXT, -- Presentada, Concedida, Denegada, Alegada
    AlegacionPresentada INTEGER, -- 0/1
    FOREIGN KEY (ConvocatoriaKey) REFERENCES DimConvocatoriaProyecto(ConvocatoriaKey),
    FOREIGN KEY (SolicitantePersonaKey) REFERENCES DimPersona(PersonaKey),
    FOREIGN KEY (ProyectoKey) REFERENCES DimProyecto(ProyectoKey)
);

CREATE TABLE DimSolicitudMovilidadOUT (
    SolicitudMovOUTKey INTEGER PRIMARY KEY,
    AlumnoPersonaKey INTEGER NOT NULL,
    CursoAcademicoSolicitud TEXT NOT NULL,
    CentroOrigenKey INTEGER,
    PlanEstudioOrigenKey INTEGER,
    ProgramaMovilidadKey INTEGER,
    UniversidadDestinoKey INTEGER,
    OrdenPreferencia INTEGER,
    IdiomaContratoEstudios TEXT,
    NivelEstudiosSolicitante TEXT,
    AreaEstudiosSolicitada TEXT,
    EstadoSolicitud TEXT, -- Presentada, Aceptada, Rechazada, Renuncia
    PreferenciaAceptada INTEGER, -- 0/1
    Renuncia INTEGER, -- 0/1
    FOREIGN KEY (AlumnoPersonaKey) REFERENCES DimPersona(PersonaKey),
    FOREIGN KEY (CentroOrigenKey) REFERENCES DimCentro(CentroKey),
    FOREIGN KEY (PlanEstudioOrigenKey) REFERENCES DimPlanEstudio(PlanEstudioKey),
    FOREIGN KEY (ProgramaMovilidadKey) REFERENCES DimProgramaMovilidad(ProgramaMovilidadKey),
    FOREIGN KEY (UniversidadDestinoKey) REFERENCES DimUniversidad(UniversidadKey)
);

-- --- Fact Tables ---

CREATE TABLE FactPersonalActivo (
    TiempoKey INTEGER NOT NULL,
    PersonaKey INTEGER NOT NULL,
    PuestoTrabajoKey INTEGER,
    CentroAdscripcionKey INTEGER,
    DepartamentoAdscripcionKey INTEGER,
    AtributosPDIKey INTEGER,
    AtributosPTGASKey INTEGER,
    NumeroEfectivos INTEGER NOT NULL DEFAULT 1, -- Count of active staff at snapshot time
    EsInvestigadorActivo INTEGER, -- 0/1
    PRIMARY KEY (TiempoKey, PersonaKey),
    FOREIGN KEY (TiempoKey) REFERENCES DimTiempo(TiempoKey),
    FOREIGN KEY (PersonaKey) REFERENCES DimPersona(PersonaKey),
    FOREIGN KEY (PuestoTrabajoKey) REFERENCES DimPuestoTrabajo(PuestoKey),
    FOREIGN KEY (CentroAdscripcionKey) REFERENCES DimCentro(CentroKey),
    FOREIGN KEY (DepartamentoAdscripcionKey) REFERENCES DimDepartamento(DepartamentoKey),
    FOREIGN KEY (AtributosPDIKey) REFERENCES DimAtributosPDI(AtributosPDIKey),
    FOREIGN KEY (AtributosPTGASKey) REFERENCES DimAtributosPTGAS(AtributosPTGASKey)
);

CREATE TABLE FactPuestos (
    TiempoKey INTEGER NOT NULL,
    PuestoKey INTEGER NOT NULL,
    PersonaOcupanteKey INTEGER,
    SituacionPuesto TEXT, -- Ocupado por titular, Vacante Técnica, Vacante Efectiva, Fuera RPT
    DesempenoPuesto TEXT, -- Titular, No Titular, Sin ocupante
    NumeroPuestos INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (TiempoKey, PuestoKey),
    FOREIGN KEY (TiempoKey) REFERENCES DimTiempo(TiempoKey),
    FOREIGN KEY (PuestoKey) REFERENCES DimPuestoTrabajo(PuestoKey),
    FOREIGN KEY (PersonaOcupanteKey) REFERENCES DimPersona(PersonaKey)
);

CREATE TABLE FactCargos (
    TiempoKey INTEGER NOT NULL,
    PersonaKey INTEGER NOT NULL,
    CargoKey INTEGER NOT NULL,
    CentroKey INTEGER,
    DepartamentoKey INTEGER,
    UnidadAdscripcion TEXT,
    NumeroCargos INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (TiempoKey, PersonaKey, CargoKey),
    FOREIGN KEY (TiempoKey) REFERENCES DimTiempo(TiempoKey),
    FOREIGN KEY (PersonaKey) REFERENCES DimPersona(PersonaKey),
    FOREIGN KEY (CargoKey) REFERENCES DimCargo(CargoKey),
    FOREIGN KEY (CentroKey) REFERENCES DimCentro(CentroKey),
    FOREIGN KEY (DepartamentoKey) REFERENCES DimDepartamento(DepartamentoKey)
);

CREATE TABLE FactMatricula (
    FactMatriculaKey INTEGER PRIMARY KEY, -- Surrogate Key
    TiempoKey INTEGER NOT NULL, -- Curso Academico
    PlanEstudioKey INTEGER NOT NULL,
    AsignaturaKey INTEGER NOT NULL,
    AlumnoPersonaKey INTEGER NOT NULL,
    CentroMatriculaKey INTEGER NOT NULL,
    AtributosAlumnoKey INTEGER,
    ProgramaMovilidadEntradaKey INTEGER, -- Null if not incoming mobility student
    GrupoAsignatura TEXT,
    NumeroVecesMatriculaAsignatura INTEGER,
    EsMatriculado INTEGER NOT NULL DEFAULT 1,
    CreditosMatriculados REAL,
    EsMovilidadSalida INTEGER, -- 0/1
    FOREIGN KEY (TiempoKey) REFERENCES DimTiempo(TiempoKey),
    FOREIGN KEY (PlanEstudioKey) REFERENCES DimPlanEstudio(PlanEstudioKey),
    FOREIGN KEY (AsignaturaKey) REFERENCES DimAsignatura(AsignaturaKey),
    FOREIGN KEY (AlumnoPersonaKey) REFERENCES DimPersona(PersonaKey),
    FOREIGN KEY (CentroMatriculaKey) REFERENCES DimCentro(CentroKey),
    FOREIGN KEY (AtributosAlumnoKey) REFERENCES DimAtributosAlumno(AtributosAlumnoKey),
    FOREIGN KEY (ProgramaMovilidadEntradaKey) REFERENCES DimProgramaMovilidad(ProgramaMovilidadKey)
);

CREATE TABLE FactRendimiento (
    FactRendimientoKey INTEGER PRIMARY KEY,
    FactMatriculaKey INTEGER, -- Link to enrollment event
    TiempoKey INTEGER NOT NULL, -- Curso Academico Evaluacion
    PlanEstudioKey INTEGER NOT NULL,
    AsignaturaKey INTEGER NOT NULL,
    AlumnoPersonaKey INTEGER NOT NULL,
    CentroMatriculaKey INTEGER NOT NULL,
    AtributosAlumnoKey INTEGER,
    Calificacion TEXT, -- Aprobado, Suspenso, NP, MH, etc.
    NotaNumerica REAL,
    RangoNotaNumerica TEXT,
    ConvocatoriasConsumidas INTEGER,
    TipoReconocimiento TEXT, -- Reconocida, Adaptada, Convalidada
    CreditosEvaluados REAL,
    CreditosSuperados REAL,
    CreditosPresentados REAL,
    CreditosSuspendidos REAL,
    CreditosReconocidos REAL,
    EsAlumnoEvaluado INTEGER, -- 0/1
    EsAlumnoSuperado INTEGER, -- 0/1
    EsAlumnoPresentado INTEGER, -- 0/1
    NotaMediaAdmisionAlumno REAL,
    MediaConvocatoriasConsumidasHastaSuperar REAL,
    FOREIGN KEY (FactMatriculaKey) REFERENCES FactMatricula(FactMatriculaKey),
    FOREIGN KEY (TiempoKey) REFERENCES DimTiempo(TiempoKey),
    FOREIGN KEY (PlanEstudioKey) REFERENCES DimPlanEstudio(PlanEstudioKey),
    FOREIGN KEY (AsignaturaKey) REFERENCES DimAsignatura(AsignaturaKey),
    FOREIGN KEY (AlumnoPersonaKey) REFERENCES DimPersona(PersonaKey),
    FOREIGN KEY (CentroMatriculaKey) REFERENCES DimCentro(CentroKey),
    FOREIGN KEY (AtributosAlumnoKey) REFERENCES DimAtributosAlumno(AtributosAlumnoKey)
);

CREATE TABLE FactEgresados (
    FactEgresadosKey INTEGER PRIMARY KEY,
    AlumnoPersonaKey INTEGER NOT NULL,
    PlanEstudioKey INTEGER NOT NULL,
    TiempoAccesoKey INTEGER, -- Curso Academico Acceso
    TiempoEgresoKey INTEGER NOT NULL, -- Curso Academico Egreso
    TipoEgreso TEXT, -- Graduado, Abandono, Traslado, Permanencia
    EsEgresado INTEGER NOT NULL DEFAULT 1,
    EsGraduado INTEGER, -- 0/1
    EsAbandonoInterrupcion INTEGER, -- 0/1
    EsTrasladoOtraUniversidad INTEGER, -- 0/1
    DuracionEstudiosAnios REAL,
    NumeroCursosMatriculados INTEGER,
    TotalCreditosMatriculados REAL,
    FOREIGN KEY (AlumnoPersonaKey) REFERENCES DimPersona(PersonaKey),
    FOREIGN KEY (PlanEstudioKey) REFERENCES DimPlanEstudio(PlanEstudioKey),
    FOREIGN KEY (TiempoAccesoKey) REFERENCES DimTiempo(TiempoKey),
    FOREIGN KEY (TiempoEgresoKey) REFERENCES DimTiempo(TiempoKey)
);

CREATE TABLE FactAdmision (
    FactAdmisionKey INTEGER PRIMARY KEY,
    SolicitudAdmisionKey INTEGER NOT NULL,
    TiempoKey INTEGER NOT NULL, -- Curso Academico Admision
    SolicitudesPreferencias INTEGER NOT NULL DEFAULT 1,
    NotaMediaAdmisionSolicitud REAL,
    EsAdmitido INTEGER, -- 0/1
    EsMatriculadoNuevoIngreso INTEGER, -- 0/1
    FOREIGN KEY (SolicitudAdmisionKey) REFERENCES DimSolicitudAdmision(SolicitudAdmisionKey),
    FOREIGN KEY (TiempoKey) REFERENCES DimTiempo(TiempoKey)
);

CREATE TABLE FactOfertaPlazas (
    TiempoKey INTEGER NOT NULL, -- Curso Academico
    PlanEstudioKey INTEGER NOT NULL,
    CupoAdjudicacion TEXT NOT NULL,
    TipoAccesoOferta TEXT, -- Preinscripcion/AccesoCiclos
    PlazasOfertadas INTEGER,
    PlazasMatriculadasNuevoIngreso INTEGER,
    PlazasSolicitadas INTEGER,
    NotaCorteAdjudicacion1 REAL,
    NotaCorteDefinitiva1 REAL,
    NotaCorteAdjudicacion2 REAL,
    NotaCorteDefinitiva2 REAL,
    PRIMARY KEY (TiempoKey, PlanEstudioKey, CupoAdjudicacion, TipoAccesoOferta),
    FOREIGN KEY (TiempoKey) REFERENCES DimTiempo(TiempoKey),
    FOREIGN KEY (PlanEstudioKey) REFERENCES DimPlanEstudio(PlanEstudioKey)
);

CREATE TABLE FactDocenciaAsignatura (
    FactDocenciaAsignaturaKey INTEGER PRIMARY KEY,
    TiempoKey INTEGER NOT NULL, -- Curso Academico
    AsignaturaKey INTEGER NOT NULL,
    NumeroGruposActividadFormativa INTEGER,
    NumeroHorasEncargo REAL,
    FOREIGN KEY (TiempoKey) REFERENCES DimTiempo(TiempoKey),
    FOREIGN KEY (AsignaturaKey) REFERENCES DimAsignatura(AsignaturaKey)
);

CREATE TABLE FactDocenciaPDI (
    FactDocenciaPDIKey INTEGER PRIMARY KEY,
    TiempoKey INTEGER NOT NULL, -- Curso Academico
    AsignaturaKey INTEGER NOT NULL,
    ProfesorPersonaKey INTEGER NOT NULL,
    TipoDocenciaKey INTEGER,
    ResponsabilidadKey INTEGER,
    HorasDocenciaImpartida REAL,
    HorasAsignaturasEspeciales REAL,
    FOREIGN KEY (TiempoKey) REFERENCES DimTiempo(TiempoKey),
    FOREIGN KEY (AsignaturaKey) REFERENCES DimAsignatura(AsignaturaKey),
    FOREIGN KEY (ProfesorPersonaKey) REFERENCES DimPersona(PersonaKey),
    FOREIGN KEY (TipoDocenciaKey) REFERENCES DimTipoDocencia(TipoDocenciaKey),
    FOREIGN KEY (ResponsabilidadKey) REFERENCES DimResponsabilidadDocente(ResponsabilidadKey)
);

CREATE TABLE FactAcuerdosBilateral (
    TiempoKey INTEGER NOT NULL, -- Curso Academico Vigencia
    AcuerdoBilateralKey INTEGER NOT NULL,
    Colectivo TEXT, -- Alumnos/Docentes
    EntradaSalida TEXT, -- IN/OUT
    PlazasOfertadas INTEGER,
    PlazasAsignadasOUT INTEGER,
    NumeroAcuerdos INTEGER NOT NULL DEFAULT 1,
    PRIMARY KEY (TiempoKey, AcuerdoBilateralKey, Colectivo, EntradaSalida),
    FOREIGN KEY (TiempoKey) REFERENCES DimTiempo(TiempoKey),
    FOREIGN KEY (AcuerdoBilateralKey) REFERENCES DimAcuerdoBilateral(AcuerdoBilateralKey)
);

CREATE TABLE FactEstudiantesIN (
    FactEstINKey INTEGER PRIMARY KEY,
    TiempoKey INTEGER NOT NULL, -- Curso Academico Estancia
    AlumnoPersonaKey INTEGER NOT NULL,
    CentroAcogidaKey INTEGER,
    ProgramaMovilidadKey INTEGER,
    UniversidadOrigenKey INTEGER,
    TotalEstudiantesIN INTEGER NOT NULL DEFAULT 1,
    DuracionEstanciaMeses REAL,
    CreditosMatriculadosEstancia REAL,
    CreditosSuperadosEstancia REAL,
    FOREIGN KEY (TiempoKey) REFERENCES DimTiempo(TiempoKey),
    FOREIGN KEY (AlumnoPersonaKey) REFERENCES DimPersona(PersonaKey),
    FOREIGN KEY (CentroAcogidaKey) REFERENCES DimCentro(CentroKey),
    FOREIGN KEY (ProgramaMovilidadKey) REFERENCES DimProgramaMovilidad(ProgramaMovilidadKey),
    FOREIGN KEY (UniversidadOrigenKey) REFERENCES DimUniversidad(UniversidadKey)
);

CREATE TABLE FactEstudiantesOUT (
    FactEstOUTKey INTEGER PRIMARY KEY,
    TiempoKey INTEGER NOT NULL, -- Curso Academico Estancia
    AlumnoPersonaKey INTEGER NOT NULL,
    CentroOrigenKey INTEGER,
    PlanEstudioOrigenKey INTEGER,
    ProgramaMovilidadKey INTEGER,
    UniversidadDestinoKey INTEGER,
    SolicitudMovOUTKey INTEGER, -- Link to the specific application preference
    TotalEstudiantesOUT INTEGER NOT NULL DEFAULT 1,
    DuracionEstanciaMeses REAL,
    CreditosSuperadosEstancia REAL,
    FOREIGN KEY (TiempoKey) REFERENCES DimTiempo(TiempoKey),
    FOREIGN KEY (AlumnoPersonaKey) REFERENCES DimPersona(PersonaKey),
    FOREIGN KEY (CentroOrigenKey) REFERENCES DimCentro(CentroKey),
    FOREIGN KEY (PlanEstudioOrigenKey) REFERENCES DimPlanEstudio(PlanEstudioKey),
    FOREIGN KEY (ProgramaMovilidadKey) REFERENCES DimProgramaMovilidad(ProgramaMovilidadKey),
    FOREIGN KEY (UniversidadDestinoKey) REFERENCES DimUniversidad(UniversidadKey),
    FOREIGN KEY (SolicitudMovOUTKey) REFERENCES DimSolicitudMovilidadOUT(SolicitudMovOUTKey)
);

CREATE TABLE FactSolicitudesMovilidadOUT (
    FactSolMovOUTKey INTEGER PRIMARY KEY,
    SolicitudMovOUTKey INTEGER NOT NULL,
    TiempoKey INTEGER NOT NULL, -- Curso Academico Solicitud
    TotalSolicitudesPreferencias INTEGER NOT NULL DEFAULT 1,
    TotalSolicitudesAceptadas INTEGER, -- 0/1
    TotalRenuncias INTEGER, -- 0/1
    FOREIGN KEY (SolicitudMovOUTKey) REFERENCES DimSolicitudMovilidadOUT(SolicitudMovOUTKey),
    FOREIGN KEY (TiempoKey) REFERENCES DimTiempo(TiempoKey)
);

CREATE TABLE FactGruposInvestigacion (
    TiempoKey INTEGER NOT NULL, -- Year
    GrupoInvKey INTEGER NOT NULL,
    NumeroGrupos INTEGER NOT NULL DEFAULT 1,
    NumeroInvestigadoresGrupo INTEGER,
    ImporteAnualConcedidoGrupo REAL,
    PRIMARY KEY (TiempoKey, GrupoInvKey),
    FOREIGN KEY (TiempoKey) REFERENCES DimTiempo(TiempoKey),
    FOREIGN KEY (GrupoInvKey) REFERENCES DimGrupoInvestigacion(GrupoInvKey)
);

CREATE TABLE FactIndicesBibliometricos (
    TiempoKey INTEGER NOT NULL, -- Year
    RevistaKey INTEGER NOT NULL,
    MateriaKey INTEGER NOT NULL,
    FactorImpactoJCR REAL,
    Cuartil INTEGER,
    Decil INTEGER,
    PRIMARY KEY (TiempoKey, RevistaKey, MateriaKey),
    FOREIGN KEY (TiempoKey) REFERENCES DimTiempo(TiempoKey),
    FOREIGN KEY (RevistaKey) REFERENCES DimRevista(RevistaKey),
    FOREIGN KEY (MateriaKey) REFERENCES DimMateriaJCR(MateriaKey)
);

CREATE TABLE FactMatriculaEEPP (
    FactMatriEEPPKey INTEGER PRIMARY KEY,
    TiempoKey INTEGER NOT NULL, -- Curso Academico
    AlumnoPersonaKey INTEGER NOT NULL,
    EstudioPropioKey INTEGER NOT NULL,
    AlumnosMatriculados INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (TiempoKey) REFERENCES DimTiempo(TiempoKey),
    FOREIGN KEY (AlumnoPersonaKey) REFERENCES DimPersona(PersonaKey),
    FOREIGN KEY (EstudioPropioKey) REFERENCES DimEstudioPropio(EstudioPropioKey)
);

CREATE TABLE FactMovilidadIDI (
    FactMovIDIKey INTEGER PRIMARY KEY,
    InvestigadorPersonaKey INTEGER NOT NULL,
    TiempoInicioKey INTEGER, -- Start Date
    TiempoFinKey INTEGER, -- End Date
    TipoEntidadOrigenKey INTEGER,
    TipoMovilidadIDI TEXT, -- Estancia/Vinculación
    MovilidadCount INTEGER NOT NULL DEFAULT 1,
    DuracionSemanas REAL,
    EsProrroga INTEGER, -- 0/1
    FOREIGN KEY (InvestigadorPersonaKey) REFERENCES DimPersona(PersonaKey),
    FOREIGN KEY (TiempoInicioKey) REFERENCES DimTiempo(TiempoKey),
    FOREIGN KEY (TiempoFinKey) REFERENCES DimTiempo(TiempoKey),
    FOREIGN KEY (TipoEntidadOrigenKey) REFERENCES DimTipoEntidad(TipoEntidadKey)
);

CREATE TABLE FactProduccionPublicacion (
    FactProdPublKey INTEGER PRIMARY KEY,
    AutorPersonaKey INTEGER NOT NULL,
    PublicacionKey INTEGER NOT NULL,
    TiempoKey INTEGER NOT NULL, -- Year of Publication
    -- Metrics could be added here
    FOREIGN KEY (AutorPersonaKey) REFERENCES DimPersona(PersonaKey),
    FOREIGN KEY (PublicacionKey) REFERENCES DimPublicacion(PublicacionKey),
    FOREIGN KEY (TiempoKey) REFERENCES DimTiempo(TiempoKey)
);

CREATE TABLE FactProduccionCongreso (
    FactProdCongKey INTEGER PRIMARY KEY,
    AutorPersonaKey INTEGER NOT NULL,
    CongresoKey INTEGER NOT NULL,
    TipoActividadKey INTEGER NOT NULL,
    TiempoKey INTEGER NOT NULL, -- Year of Congress
    ActividadesCongreso INTEGER NOT NULL DEFAULT 1,
    FOREIGN KEY (AutorPersonaKey) REFERENCES DimPersona(PersonaKey),
    FOREIGN KEY (CongresoKey) REFERENCES DimCongreso(CongresoKey),
    FOREIGN KEY (TipoActividadKey) REFERENCES DimTipoActividadCongreso(TipoActividadKey),
    FOREIGN KEY (TiempoKey) REFERENCES DimTiempo(TiempoKey)
);

CREATE TABLE FactProyectos (
    FactProyectosKey INTEGER PRIMARY KEY,
    ProyectoKey INTEGER NOT NULL,
    TiempoKey INTEGER NOT NULL, -- Year of activity/concession
    EsProyectoVigente INTEGER, -- 0/1
    EsProyectoNuevo INTEGER, -- 0/1
    ImporteConcedido REAL,
    IngresosTotales REAL,
    IngresosIVA REAL,
    IngresosOverhead REAL,
    IngresosProyecto REAL,
    CostesTotalesGasto REAL,
    CostesIVA REAL,
    CostesAlProyecto REAL,
    FOREIGN KEY (ProyectoKey) REFERENCES DimProyecto(ProyectoKey),
    FOREIGN KEY (TiempoKey) REFERENCES DimTiempo(TiempoKey)
);

CREATE TABLE FactSolicitudesConvocatoria (
    FactSolConvKey INTEGER PRIMARY KEY,
    SolicitudProyKey INTEGER NOT NULL,
    TiempoKey INTEGER NOT NULL, -- Year of Resolution?
    TotalSolicitudes INTEGER NOT NULL DEFAULT 1,
    ImporteSolicitado REAL,
    ImporteConcedido REAL,
    SolicitudesConcedidas INTEGER, -- 0/1
    SolicitudesDenegadas INTEGER, -- 0/1
    FOREIGN KEY (SolicitudProyKey) REFERENCES DimSolicitudProyecto(SolicitudProyKey),
    FOREIGN KEY (TiempoKey) REFERENCES DimTiempo(TiempoKey)
);


