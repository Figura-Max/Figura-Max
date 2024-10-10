function [xout tout flag] = RKF45(f, t0, x0, T, tolmin, tolmax, hmin, hmax)
    # flag = 0: Success, all tolerances reached
    # flag > 0: Failure, at least one tolerance not reached (number of bad steps)

    if (tolmin >= tolmax || tolmin < 0)
        disp('Choose 0 < tolmin < tolmax. Exiting...');
        return;
    end

    if (hmin >= hmax || hmin < 0)
        disp('Choose 0 < hmin < hmax. Exiting...');
        return;
    end

    if (T <= t0)
        disp('Choose T > t0. Exiting...');
        return;
    end

    flag = 0; # Start assuming success

    tout = [t0];
    xout = [x0];

    t = t0;
    x = x0;
    force_small_h = 1;
    h = hmax; # Start with the largest possible stepsize

    while (t < T)
        if (t + h > T)
            h = T - t;
            force_small_h = 0;
        end

        if (h < hmin && force_small_h == 1)
            h = hmin;
        elseif (h > hmax)
            h = hmax;
        end

        told = t;
        xold = x;

        [x t errest] = RKF45_step(f, t, x, h);

        if (errest <= tolmax)
            tout = [tout t];
            xout = [xout x];
            if (errest < tolmin)
                h = 2*h;
            end
        else
            if (h > hmin)
                h = h/2;
                t = told;
                x = xold;
            else
                flag = flag + 1;   # Can't reach this tolerance
                tout = [tout t];
                xout = [xout x];
            end
        end
    end

    if (nargout == 0)
        plot(tout, xout)
    end
endfunction


function [xnew tnew errest] = RKF45_step(f, t, x, h)
    k1 = f(t          , x);
    k2 = f(t +   1/4*h, x + h*k1/4);
    k3 = f(t +   3/8*h, x + h*(3*k1 + 9*k2)/32);
    k4 = f(t + 12/13*h, x + h*(1932*k1 - 7200*k2 + 7296*k3)/2197);
    k5 = f(t +       h, x + h*(8341*k1 - 32832*k2 + 29440*k3- 845*k4)/4104);
    k6 = f(t +   1/2*h, x + h*(-6080*k1 + 41040*k2 - 28352*k3 + 9295*k4 - 5643*k5)/20520);

    tnew = t + h;

    # Using the 4th-order method
    #xnew = x + h*(2375*k1 + 11264*k3 + 10985*k4 - 4104*k5)/20520;

    # Using the 5th-order method
    xnew = x + h*(33440*k1 + 146432*k3 + 142805*k4 - 50787*k5 + 10260*k6)/282150;

    # Error estimate
    errest = h*norm((1045*k1 - 11264*k3 - 10985*k4 + 7524*k5 + 13680*k6)/376200, "inf");
endfunction
