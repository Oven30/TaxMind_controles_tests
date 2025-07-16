Feature: Concatenar columnas

  Scenario: Concatenar dos columnas con guion
    Given que tengo un DataFrame con las columnas "A" y "B"
      | A   | B     |
      | uno | dos   |
      | tres| cuatro|
    When concateno las columnas ["A", "B"] en "Concatenado" usando el separador "-"
    Then la columna "Concatenado" debe ser
      | Concatenado |
      | uno-dos     |
      | tres-cuatro |

  Scenario: Concatenar tres columnas sin separador
    Given que tengo un DataFrame con las columnas "X", "Y", "Z"
      | X | Y | Z |
      | a | b | c |
      | d | e | f |
    When concateno las columnas ["X", "Y", "Z"] en "Junto" usando el separador ""
    Then la columna "Junto" debe ser
      | Junto |
      | abc   |
      | def   |