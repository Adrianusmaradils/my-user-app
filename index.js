cat << 'EOF' > src/index.js
export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;
    const method = request.method;

    const headers = {
      'Content-Type': 'application/json',
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
    };

    if (method === 'OPTIONS') {
      return new Response(null, { headers });
    }

    try {
      // 1. GET /api/users - Ambil semua daftar user
      if (path === '/api/users' && method === 'GET') {
        const { results } = await env.Adrianusmaradils.prepare('SELECT * FROM users ORDER BY id DESC').all();
        return Response.json({ success: true, data: results }, { headers });
      }

      // 2. POST /api/users - Tambah user baru
      if (path === '/api/users' && method === 'POST') {
        const body = await request.json();
        const { username, email, full_name, role } = body;
        if (!username || !email || !full_name) {
          return Response.json({ success: false, message: 'Data tidak lengkap' }, { status: 400, headers });
        }
        await env.Adrianusmaradils.prepare(
          'INSERT INTO users (username, email, full_name, role) VALUES (?, ?, ?, ?)'
        ).bind(username, email, full_name, role || 'user').run();
        return Response.json({ success: true, message: 'User berhasil ditambahkan' }, { status: 201, headers });
      }

      // 3. PUT /api/users/:id - Update / Edit data user berdasarkan ID
      if (path.startsWith('/api/users/') && method === 'PUT') {
        const id = path.split('/')[3];
        const body = await request.json();
        const { username, email, full_name, role } = body;
        
        await env.Adrianusmaradils.prepare(
          'UPDATE users SET username = ?, email = ?, full_name = ?, role = ? WHERE id = ?'
        ).bind(username, email, full_name, role, id).run();
        
        return Response.json({ success: true, message: 'User berhasil diperbarui' }, { headers });
      }

      // 4. DELETE /api/users/:id - Hapus user berdasarkan ID
      if (path.startsWith('/api/users/') && method === 'DELETE') {
        const id = path.split('/')[3];
        await env.Adrianusmaradils.prepare('DELETE FROM users WHERE id = ?').bind(id).run();
        return Response.json({ success: true, message: 'User berhasil dihapus' }, { headers });
      }

      return Response.json({ success: false, message: 'Endpoint tidak ditemukan' }, { status: 404, headers });

    } catch (error) {
      return Response.json({ success: false, error: error.message }, { status: 500, headers });
    }
  }
};
EOF
