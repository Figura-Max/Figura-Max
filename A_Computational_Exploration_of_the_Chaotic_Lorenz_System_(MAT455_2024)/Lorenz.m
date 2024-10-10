function Lorenz()
    h = 1e-14;
    sig = 10;
    bet = 8/3;
    rho = 28;
    #x0 = [-8; 8; 27];
    #x0 = [-2.147367631; 2.078048211; 27];
    #x0 = [6*sqrt(2); 6*sqrt(2); 27];
    #x0 = [0; 1; 0];
    x0 = [40; 40; 27];
    T = 50;
    
    #x0(1)-=1e-6;
    
    f = @(t,x) [-sig*x(1) + sig*x(2); rho*x(1) - x(2) - x(1).*x(3); -bet*x(3) + x(1).*x(2)];
    
    tic
    #[xoutE, toutE] = Euler(f, 0, x0, T, h);
    #[xoutE, toutE] = EulerImproved(f, 0, x0, T, h);
    #[xoutE, toutE] = RK4(f, 0, x0, T, h);
    #[xoutE, toutE, flags] = RKF45(f, 0, x0, T, h/10, h*10, 1e-4, 1e-1);
    [xoutE, toutE, flags] = DP45(f, 0, x0, T, h/10, h*10, 1e-4, 1e-1);
    #[xoutE, toutE] = EulerImplicit(f, 0, x0, T, h);
    #[xoutE, toutE] = EulerImprovedImplicit(f, 0, x0, T, h);
    toc
    
    flags
    
    name = sprintf("Lorenz System with DP45 method, error ~%1.0e",h);
    plot(toutE(:),xoutE(1,:));
    #xlim([0, T])
    title(name);
    xlabel("t");
    legend("x");
    print(sprintf("Lorenz_farout1_%1.0e_x.png",h));
    plot(toutE,xoutE);
    #xlim([0, T])
    title(name);
    xlabel("t");
    legend("x","y","z");
    print(sprintf("Lorenz_farout1_%1.0e_xyz.png",h));
    plot(xoutE(1,:),xoutE(2,:));
    title(name);
    xlabel("x"); ylabel("y");
    print(sprintf("Lorenz_farout1_%1.0e_parxy.png",h));
    plot(xoutE(1,:),xoutE(3,:));
    title(name);
    xlabel("x"); ylabel("z");
    print(sprintf("Lorenz_farout1_%1.0e_parxz.png",h));
    plot(xoutE(2,:),xoutE(3,:));
    title(name);
    xlabel("y"); ylabel("z");
    print(sprintf("Lorenz_farout1_%1.0e_paryz.png",h));
    plot3(xoutE(1,:),xoutE(2,:),xoutE(3,:));
    title(name);
    xlabel("x"); ylabel("y"); zlabel("z");
    print(sprintf("Lorenz_farout1_%1.0e_parxyz.png",h));
    plot3(xoutE(1,:),xoutE(2,:),xoutE(3,:),
        xoutE(1,:),xoutE(2,:),min(xoutE(3,:))*ones(1,size(xoutE)(2)),
        xoutE(1,:),max(xoutE(2,:))*ones(1,size(xoutE)(2)),xoutE(3,:),
        max(xoutE(1,:))*ones(1,size(xoutE)(2)),xoutE(2,:),xoutE(3,:));
    #title(name);
    #xlabel("x"); ylabel("y"); zlabel("z");
endfunction
