function Beam_Deflect(n, shap, attach)
    L = 10;         #10 meter length
    if shap==0          #Hollow square
        A = 8.25e-2;        #Outer size 8.25 cm
        a = 4.25e-2;        #Inner size 4.25 cm
        S = A^2-a^2;        #Cross-sectional area
        I = (A^4-a^4)/12;   #Second Moment of Inertia
    elseif shap==1          #Annulus
        R = 4.987e-2;       #Outer size 4.987 cm
        r = 2.992e-2;       #Inner size 2.992 cm
        S = pi*(R^2-r^2);   #Cross-sectional area
        I = pi*(R^4-r^4)/4; #Second Moment of Inertia
    end
    E = 6.9e10;     #Young's modulus - 69GPa
    rho = 2700;     #Mass density in kg/m^3
    g = 9.81;       #Gravitational acceleration
    w = S*rho*g;    #Force of gravity by length
    #n = 10;        #Precision determined by user
    h = L/n;
    N = n + 1;
    
    #"Output" vector
    f = -h^4/(E*I) * w * ones(N, 1);
    f(1) = f(2) = f(N-1) = f(N) = 0;
    if attach==2
        f(N) = 3*f(N-2)/2;  #Right end free
    end
    f
    % Define the matrix of the system. Notation: d0 is the main diagonal;
    % dpn is superdiagonal n; dmn is subdiagonal n
    d0 = 6*ones(1, N);
    dp1 = dm1 = -4*ones(1, N-1);
    dp2 = dm2 = ones(1, N-2);
    #Left end fixed
    d0(1) = 1.0; d0(2) = 4.0;
    dp1(1) = 0.0; dp1(2) = -1.0;
    dp2(1) = 0.0; dp2(2) = 0.0;
    dm1(1) = 0.0;
    dm2(1) = 0.0;
    if attach==1    #Right end pinned
        d0(N) = 1.0; d0(N-1) = 5.0;
        dp1(N-1) = dm1(N-1) = 0.0;
        dp2(N-2) = dm2(N-2) = 0.0;
    elseif attach==2    #Right end free
        d0(N) = 1.0; d0(N-1) = 5.0;
        dp1(N-1) = dm1(N-1) = -2.0;
    else
        printf("Invalid attach option\n")
        return
    end
    #% Fixed right end
    #d0(N) = 1.0; d0(N-1) = 4.0;
    #dp1(N-1) = 0.0;
    #dp2(N-2) = 0.0;
    #dm1(N-1) = 0.0; dm1(N-2) = -1.0;
    #dm2(N-2) = 0.0; dm2(N-3) = 0.0;
    
    #Apply system solver
    y = GaussElimPenta(dm2, dm1, d0, dp1, dp2, f);
    #Show data
    x = (0:h:L)';   #Transpose to be compatible with y
    if attach==1
        y_exact = -S*rho*g/(48*E*I)*x.^2.*(3*L^2 - 5*L*x + 2*x.^2);
    elseif attach==2
        y_exact = -S*rho*g/(24*E*I)*x.^2.*(6*L^2 - 4*L*x + x.^2);
    end
    #y_exact = -S*rho*g/(24*E*I)*x.^2.*(L - x).^2;
    err = abs(y - y_exact);
    printf("Maximum error: %.4e\n",max(err))
    subplot(2,1,1);
    plot(x, y, "b*", x, y_exact, "r")
    title('Deflection of the beam');
    xlabel('x'); ylabel('y (deflection)');
    grid on;
    subplot(2,1,2);
    plot(x, err, "r")
    title('Error: |computed - exact|');
    xlabel('x'); ylabel('Error');
    grid on;
    #print(sprintf("Beam_%d%d_%d.png",shap,attach,n)); 
endfunction
