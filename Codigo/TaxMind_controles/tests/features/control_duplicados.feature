Feature: Comparar CUITs entre dos DataFrames

  Scenario: Marcar CUITs que no están en el segundo DataFrame
    Given tengo un DataFrame con la columna "CUIT"
      | CUIT        |
      | 20123456789 |
      | 20234567890 |
      | 20345678901 |
    And el segundo DataFrame tiene la columna "CUIT"
      | CUIT        |
      | 20234567890 |
      | 20345678901 |
    When comparo la columna "CUIT" y marco en "NoEncontrado"
    Then la columna "NoEncontrado" debe ser
      | NoEncontrado |
      | 1            |
      | 0            |
      | 0            |


 Scenario: Marcar CUITs cuando ninguno coincide con el segundo DataFrame
    Given tengo un DataFrame con la columna "CUIT" 2
      | CUIT        |
      | 20123456789 |
      | 20234567890 |
      | 20345678901 |
    And el segundo DataFrame tiene la columna "CUIT" 2
      | CUIT        |
      | 20999999999 |
      | 20888888888 |
    When comparo la columna "CUIT" y marco en "NoEncontrado" 2
    Then la columna "NoEncontrado" debe ser 2
      | NoEncontrado |
      | 1            |
      | 1            |
      | 1            |


  Scenario: Marcar CUITs cuando solo uno coincide con el segundo DataFrame
    Given tengo un DataFrame con la columna "CUIT" 3
      | CUIT        |
      | 20123456789 |
      | 20234567890 |
      | 20345678901 |
    And el segundo DataFrame tiene la columna "CUIT" 3
      | CUIT        |
      | 20234567890 |
      | 20999999999 |
    When comparo la columna "CUIT" y marco en "NoEncontrado" 3
    Then la columna "NoEncontrado" debe ser
      | NoEncontrado |
      | 1            |
      | 0            |
      | 1            |