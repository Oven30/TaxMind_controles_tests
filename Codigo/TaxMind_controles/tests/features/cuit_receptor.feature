Feature: Controlar CUIT del receptor

  Scenario: Marcar filas donde el CUIT del receptor es diferente al esperado
    Given tengo un DataFrame con la columna "Cuit del Receptor"
      | Cuit del Receptor |
      | 20123456789       |
      | 20234567890       |
      | 20345678901       |
    When controlo el CUIT receptor con "20234567890"
    Then la columna "Cuit Receptor Usuario" debe ser
      | Cuit Receptor Usuario |
      | 1                    |
      | 0                    |
      | 1                    |

  Scenario: Marcar todas las filas cuando el CUIT receptor no aparece
  Given tengo un DataFrame con la columna "Cuit del Receptor" 2
    | Cuit del Receptor |
    | 20123456789       |
    | 20234567890       |
    | 20345678901       |
  When controlo el CUIT receptor con "20999999999" 2
  Then la columna "Cuit Receptor Usuario" debe ser 2
    | Cuit Receptor Usuario |
    | 1                    |
    | 1                    |
    | 1                    |

  
  Scenario: Marcar filas cuando el CUIT receptor esperado se repite
  Given tengo un DataFrame con la columna "Cuit del Receptor"
    | Cuit del Receptor |
    | 20123456789       |
    | 20234567890       |
    | 20234567890       |
    | 20345678901       |
  When controlo el CUIT receptor con "20234567890"
  Then la columna "Cuit Receptor Usuario" debe ser
    | Cuit Receptor Usuario |
    | 1                    |
    | 0                    |
    | 0                    |
    | 1                    |