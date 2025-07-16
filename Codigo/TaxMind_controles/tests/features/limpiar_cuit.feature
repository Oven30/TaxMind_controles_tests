Feature: Limpiar y validar CUIT
  Para asegurarme de que puedo limpiar un CUIT correctamente y validar su estructura
  Como administrador del sistema
  Quiero verificar que el formtato del CUIT sea el necesario

  Scenario: 1-Validar que el CUIT no tenga caracteres "-"
    Given tengo un CUIT "20-12345678-9"
    When limpio el CUIT
    Then el CUIT limpio debe ser "20123456789"

  Scenario: 2-Validar que el CUIT tenga 11 caracteres
    Given tengo un CUIT ya limpio
    Then el CUIT mide exactamente 11 caracteres


