Feature: Validar y Formatear Fecha
  Para asegurarme de que puedo validar y formatear una fecha correctamente
  Como administrador del sistema
  Quiero verificar que el formato de la fecha sea el necesario

  Scenario: Validar y formatear una fecha válida
    Given tengo una fecha "25-12-2023"
    When valido y formateo la fecha
    Then la fecha formateada debe ser "25/12/2023"

  Scenario: Validar una fecha no válida
    Given tengo una fecha no válida "30-02-2023"
    When valido y formateo la fecha no válida
    Then debería ocurrir un error de fecha no válida

  Scenario: Validar una fecha válida con puntos como separador
    Given tengo una fecha valida con puntos "23.04.2023"
    When valido y formateo la fecha
    Then la fecha formateada debe ser "23/04/2023"

  Scenario: Validar y formatear una fecha válida con coma como separador
    Given tengo una fecha con comas "23,04,2023"
    When valido y formateo la fecha con comas
    Then la fecha con comas formateada debería dar un error de fecha no válida