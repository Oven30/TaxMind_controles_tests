Feature: Controlar suma de columnas contra el total

  Scenario: Todas las filas coinciden con el total
    Given tengo un DataFrame con las columnas "A", "B" y "Total"
      | A | B | Total |
      | 2 | 3 | 5     |
      | 1 | 4 | 5     |
      | 0 | 0 | 0     |
    When controlo la suma de ["A", "B"] contra "Total" en "Control"
    Then la columna "Control" debe ser
      | Control |
      | 0       |
      | 0       |
      | 0       |

  Scenario: Algunas filas no coinciden con el total
    Given tengo un DataFrame con las columnas "A", "B" y "Total"
      | A | B | Total |
      | 2 | 3 | 5     |
      | 1 | 4 | 6     |
      | 0 | 0 | 1     |
    When controlo la suma de ["A", "B"] contra "Total" en "Control"
    Then la columna "Control" debe ser
      | Control |
      | 0       |
      | 1       |
      | 1       |


Scenario: Todas las filas tienen suma negativa y coinciden con el total negativo
  Given tengo un DataFrame con las columnas "A", "B" y "Total" negativo
    | A  | B  | Total |
    | -2 | -3 | -5    |
    | -1 | -4 | -5    |
    | -2 | -2 | -4    |
  When controlo la suma de ["A", "B"] contra "Total" en "Control" negativo
  Then la columna "Control" debe ser negativo
    | Control |
    | 0       |
    | 0       |
    | 0       |


Scenario: Una fila tiene suma negativa y el resto positiva
  Given tengo un DataFrame con las columnas "A", "B" y "Total"
    | A  | B  | Total |
    | -2 | -3 | -5    |
    |  1 |  4 |  5    |
    |  2 |  2 |  4    |
  When controlo la suma de ["A", "B"] contra "Total" en "Control"
  Then la columna "Control" debe ser
    | Control |
    | 0       |  
    | 0       |  
    | 0       | 

  