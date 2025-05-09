describe('Gestión de Sucursales', () => {
  beforeEach(() => {
    // Intercepta la solicitud GET a /sucursales que el frontend hace al backend
    cy.intercept('GET', '**/sucursales').as('getSucursales');
    cy.visit('/sucursales');
    cy.wait('@getSucursales').its('response.statusCode').should('eq', 200);
  });

  it('Carga correctamente una zona', () => {
    // Intercepta la solicitud GET a /zonas que se dispara al abrir el formulario
    cy.intercept('GET', '**/zonas').as('getZonas');
    cy.contains('button', 'Agregar').click();
    cy.wait('@getZonas').its('response.statusCode').should('eq', 200);

    cy.get('#dropdown-zona').click();
    cy.get('.custom-dropdown-item-add').click();
    cy.get('#zona').type('Zona 1');
    cy.get('.custom-add-button').click();
    cy.get('.btn-close').click();
  });

  it('Carga correctamente una sucursal', () => {
    // Intercepta la solicitud GET a /zonas
    cy.intercept('GET', '**/zonas').as('getZonas');
    cy.contains('button', 'Agregar').click();
    cy.wait('@getZonas').its('response.statusCode').should('eq', 200);

    // Completa el formulario para crear una sucursal
    cy.get('#nombre').type('Sucursal 1');
    cy.get('#dropdown-zona').click();
    cy.get('.custom-dropdown-item').contains('Zona 1').click();
    cy.get('#direccion').type('Dirección 1');
    cy.get('#superficie').type('100');

    // Intercepta la solicitud POST a /sucursales (cuando se crea la sucursal)
    cy.intercept('POST', '**/sucursales').as('createSucursal');
    cy.get('form > .btn-primary').click();
    cy.wait('@createSucursal').its('response.statusCode').should('eq', 200);

    // Vuelve a cargar la lista de sucursales
    cy.intercept('GET', '**/sucursales').as('getSucursales');
    cy.visit('/sucursales');
    cy.wait('@getSucursales').its('response.statusCode').should('eq', 200);

    // Verifica que la sucursal aparece en la tabla
    cy.get('tbody tr:last-child').within(() => {
      cy.get(':nth-child(2)').should('contain.text', 'Sucursal 1');
      cy.get(':nth-child(3)').should('contain.text', 'Zona 1');
      cy.get(':nth-child(4)').should('contain.text', 'Dirección 1');
      cy.get(':nth-child(5)').should('contain.text', '100');
    });
  });

  it('Edita correctamente una sucursal', () => {
    // Asegúrate de que haya una sucursal para editar
    cy.get('tbody tr:last-child').should('exist');

    // Intercepta la solicitud GET a /zonas (si el formulario de edición la necesita)
    cy.intercept('GET', '**/zonas').as('getZonas');
    cy.get('tr:last-child > :nth-child(6) > .btn-warning').click();
    cy.wait('@getZonas').its('response.statusCode').should('eq', 200);

    // Edita los campos
    cy.get('#nombre').clear().type('Sucursal 2');
    cy.get('#direccion').clear().type('Dirección 2');
    cy.get('#superficie').clear().type('200');

    // Intercepta la solicitud PUT o PATCH a /sucursales
    cy.intercept('PUT', '**/sucursales/*').as('updateSucursal');
    cy.get('form > .btn').click();
    cy.wait('@updateSucursal').its('response.statusCode').should('eq', 200);

    // Vuelve a cargar la lista de sucursales
    cy.intercept('GET', '**/sucursales').as('getSucursales');
    cy.visit('/sucursales');
    cy.wait('@getSucursales').its('response.statusCode').should('eq', 200);

    // Verifica los cambios
    cy.get('tbody tr:last-child').within(() => {
      cy.get(':nth-child(2)').should('contain.text', 'Sucursal 2');
      cy.get(':nth-child(4)').should('contain.text', 'Dirección 2');
      cy.get(':nth-child(5)').should('contain.text', '200');
    });
  });

  it('Elimina correctamente una sucursal', () => {
    // Asegúrate de que haya una sucursal para eliminar
    cy.get('tbody tr:last-child').should('exist');

    // Intercepta la solicitud DELETE a /sucursales
    cy.intercept('DELETE', '**/sucursales/*').as('deleteSucursal');
    cy.get('tr:last-child > :nth-child(6) > .btn-danger').click();
    cy.wait('@deleteSucursal').its('response.statusCode').should('eq', 200);

    // Vuelve a cargar la lista de sucursales
    cy.intercept('GET', '**/sucursales').as('getSucursales');
    cy.visit('/sucursales');
    cy.wait('@getSucursales').its('response.statusCode').should('eq', 200);

    // Verifica que la tabla esté vacía o que la sucursal ya no esté
    cy.get('tbody tr').should('have.length', 0);
  });

  it('Elimina correctamente una zona', () => {
    // Intercepta la solicitud GET a /zonas
    cy.intercept('GET', '**/zonas').as('getZonas');
    cy.contains('button', 'Agregar').click();
    cy.wait('@getZonas').its('response.statusCode').should('eq', 200);

    cy.get('#dropdown-zona').click();
    
    cy.intercept('DELETE', '**/zonas/*').as('deleteZona');
    cy.get('.custom-delete-button').click();
    cy.wait('@deleteZona').its('response.statusCode').should('eq', 200);

    cy.get('.btn-close').click();
  });
});