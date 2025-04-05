describe('Login Page', () => {
    it('should display login title', () => {
        cy.visit('/login');
        cy.contains('Iniciar Sesión');
    });
});
