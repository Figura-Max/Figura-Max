function x = GaussElimPenta(e, a, d, c, f, b)
    n = length(b);
    xmult = 0.0;
    for k = 1:(n-2)
        xmult = a(k)/d(k);
        d(k+1)-=xmult*c(k);
        c(k+1)-=xmult*f(k);
        b(k+1)-=xmult*b(k);
        xmult = e(k)/d(k);
        a(k+1)-=xmult*c(k);
        d(k+2)-=xmult*f(k);
        b(k+2)-=xmult*b(k);
    end
    xmult = a(n-1)/d(n-1);
    d(n)-=xmult*c(n-1);
    b(n)-=xmult*b(n-1);
    
    x = zeros([n,1]);
    x(n) = b(n)/d(n);
    x(n-1) = (b(n-1) - c(n-1)*x(n)) / d(n-1);
    for i = (n-2):-1:1
        x(i) = (b(i) - c(i)*x(i+1) - f(i)*x(i+2)) / d(i);
    end
endfunction
