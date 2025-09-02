import ccxt
import time
import pandas as pd
import os

def run_bot():
    # Conexión a Binance con API Key y Secret
    exchange = ccxt.binance({
        'apiKey': os.getenv('BINANCE_API_KEY'),
        'secret': os.getenv('BINANCE_API_SECRET'),
        'enableRateLimit': True,
    })
    
    symbol = 'XMR/USDT'  # Puedes cambiar a BTC/USDT, ETH/USDT, etc.
    amount = 10  # Cantidad en USDT por operación (ajusta según tu capital)
    
    print("🤖 Bot de trading automático iniciado...")
    in_position = False  # Para evitar múltiples compras

    while True:
        try:
            # Obtener velas (1h)
            ohlcv = exchange.fetch_ohlcv(symbol, '1h', limit=100)
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            close = df['close']

            # Calcular medias móviles
            sma10 = close.rolling(10).mean().iloc[-1]
            sma30 = close.rolling(30).mean().iloc[-1]
            sma10_prev = close.rolling(10).mean().iloc[-2]
            sma30_prev = close.rolling(30).mean().iloc[-2]

            precio_actual = close.iloc[-1]

            # Señal de COMPRA: SMA10 cruza arriba de SMA30
            if sma10 > sma30 and sma10_prev <= sma30_prev and not in_position:
                print(f"🟢 COMPRA | {time.strftime('%H:%M')} | Precio: {precio_actual:.2f} USDT")
                # Descomenta para operar en real:
                # order = exchange.create_market_buy_order(symbol, amount / precio_actual)
                in_position = True

            # Señal de VENTA: SMA10 cruza abajo de SMA30
            elif sma10 < sma30 and sma10_prev >= sma30_prev and in_position:
                print(f"🔴 VENTA | {time.strftime('%H:%M')} | Precio: {precio_actual:.2f} USDT")
                # Descomenta para operar en real:
                # order = exchange.create_market_sell_order(symbol, amount / precio_actual)
                in_position = False

            else:
                print(f"🟡 Esperando... | {time.strftime('%H:%M')} | Precio: {precio_actual:.2f} USDT")

        except Exception as e:
            print(f"❌ Error: {e}")

        time.sleep(60)  # Espera 60 segundos antes de revisar

if __name__ == "__main__":
    run_bot()
